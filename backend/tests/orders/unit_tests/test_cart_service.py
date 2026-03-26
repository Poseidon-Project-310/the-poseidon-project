# backend/tests/orders/unit_tests/test_cart_service.py
import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from backend.services.cart_service import CartService
from backend.schemas.cart_schema import Cart
from backend.schemas.order_schema import OrderItem, OrderItemCreate, OrderItemUpdate


# --- Fixtures ---

@pytest.fixture
def mock_user_repo():
    """Creates a fake User Repository with one test user."""
    repo = MagicMock()
    # By default, load_all returns a list with one user who has an empty cart
    repo.load_all.return_value = [
        {
            "id": "brady_123",
            "name": "Brady",
            "cart": {"items": []}
        }
    ]
    return repo

@pytest.fixture
def service(mock_user_repo):
    """Injects the fake repo into the CartService."""
    return CartService(user_repository=mock_user_repo)

# --- Get Cart Tests ---

def test_get_cart_success(service, mock_user_repo):
    """
    Equivalence Partitioning
    Test getting a cart for an existing user.
    """
    result = service.get_cart("brady_123")
    
    assert isinstance(result, Cart)
    assert len(result.items) == 0

def test_get_cart_not_found(service):
    """
    Fault Injection / Exception Handling
    Ensure a 404 is thrown if the user ID doesn't exist.
    """
    with pytest.raises(HTTPException) as exc:
        service.get_cart("fake_user_999")
        
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"

def test_get_cart_no_cart_key(service, mock_user_repo):
    """
    Boundary Value Analysis / Edge Case
    If the user exists but the 'cart' key hasn't been created yet, 
    it should default to an empty cart safely.
    """
    mock_user_repo.load_all.return_value = [{"id": "brady_123", "name": "Brady"}] # No 'cart' key
    
    result = service.get_cart("brady_123")
    
    assert isinstance(result, Cart)
    assert len(result.items) == 0

# --- Add Item Tests ---

def test_add_new_item(service, mock_user_repo):
    """
    Equivalence Partitioning
    Test adding an item that isn't in the cart yet.
    """
    new_item = OrderItem(menu_item_id=1, quantity=2, price_at_time=15.0)
    
    result = service.add_item("brady_123", new_item)
    
    assert len(result.items) == 1
    assert result.items[0].menu_item_id == 1
    assert result.items[0].quantity == 2
    mock_user_repo.save_all.assert_called_once()

def test_add_existing_item(service, mock_user_repo):
    """
    Equivalence Partitioning
    Test adding an item that is ALREADY in the cart (should increment quantity).
    """
    # Setup the mock so the user already has 1 burger (menu_item_id=1)
    existing_cart = {"items": [{"menu_item_id": 1, "quantity": 1, "price_at_time": 10.0}]}
    mock_user_repo.load_all.return_value = [{"id": "brady_123", "cart": existing_cart}]
    
    # We add 2 MORE of the same burger
    new_item = OrderItem(menu_item_id=1, quantity=2, price_at_time=10.0)
    
    result = service.add_item("brady_123", new_item)
    
    # The cart should still only have 1 item type, but the quantity should now be 3
    assert len(result.items) == 1
    assert result.items[0].quantity == 3
    mock_user_repo.save_all.assert_called_once()

# --- Clear Cart Tests ---

def test_clear_cart(service, mock_user_repo):
    """
    Functional Test
    Ensure the cart is completely emptied out.
    """
    # Setup mock with a full cart
    full_cart = {"items": [{"menu_item_id": 1, "quantity": 5, "price_at_time": 10.0}]}
    mock_user_repo.load_all.return_value = [{"id": "brady_123", "cart": full_cart}]
    
    result = service.clear_cart("brady_123")
    
    assert len(result.items) == 0
    mock_user_repo.save_all.assert_called_once()

# --- Remove Item Tests ---

def test_remove_item(service, mock_user_repo):
    existing_cart = {"items": [{"menu_item_id": 1, "quantity": 1, "price_at_time": 10.0}]}
    mock_user_repo.load_all.return_value = [{"id": "brady_123", "cart": existing_cart}]
    
    result = service.remove_item("brady_123", 1)
    assert len(result.items) == 0

# --- Update Item Quantity Tests ---

def test_update_quantity(service, mock_user_repo):
    existing_cart = {"items": [{"menu_item_id": 1, "quantity": 1, "price_at_time": 10.0}]}
    mock_user_repo.load_all.return_value = [{"id": "brady_123", "cart": existing_cart}]
    
    result = service.update_item_quantity("brady_123", 1, 5)
    assert result.items[0].quantity == 5

# --- Save Helper Tests ---

def test_save_cart_to_user_not_found(service):
    """
    Fault Injection
    Ensure the private save helper handles a missing user properly.
    """
    fake_cart = Cart(items=[])
    
    with pytest.raises(HTTPException) as exc:
        service._save_cart_to_user("ghost_user", fake_cart)
        
    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"