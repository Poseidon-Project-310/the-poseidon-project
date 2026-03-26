# backend/tests/orders/unit_tests/test_order_service.py
import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from backend.services.order_service import OrderValidate
from backend.schemas.order_schema import OrderCreate, OrderStatus, OrderItem

# --- Fixtures ---

@pytest.fixture
def mock_repo():
    repo = MagicMock()
    repo.load_all.return_value = []
    return repo

@pytest.fixture
def service(mock_repo):
    from backend.services.order_service import OrderService
    s = OrderService(repository=mock_repo) 
    return s

# --- Validator Tests ---

@pytest.mark.parametrize("valid_lat", [90.0, -90.0, 49.9423])
def test_validate_latitude_success(valid_lat):
    """Boundary Value Analysis: Valid range [-90, 90]"""
    assert OrderValidate.validate_delivery_latitude(valid_lat) == valid_lat

@pytest.mark.parametrize("invalid_lat", [90.1, -90.1])
def test_validate_latitude_failure(invalid_lat):
    """Boundary Value Analysis: Just outside valid range"""
    with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
        OrderValidate.validate_delivery_latitude(invalid_lat)

@pytest.mark.parametrize("valid_pc", ["V1V 1V1", "V1V1V1", "v1v 1v1"])
def test_validate_postal_code_success(valid_pc):
    """Equivalence Partitioning: Valid Canadian PC formats"""
    result = OrderValidate.validate_delivery_postal_code(valid_pc)
    # Ensuring it strips and uppers correctly
    assert result == valid_pc.strip().upper()

# --- Order Creation Tests ---

def test_create_order_success(service, mock_repo):
    """
    Equivalence Partitioning
    Test creating a valid order with items.
    Returns the Order object directly.
    """
    items = [OrderItem(menu_item_id=1, quantity=1, price_at_time=10.0)]
    payload = OrderCreate(
        customer_id="brady_123",
        restaurant_id=1,
        items=items,
        delivery_latitude=49.8,
        delivery_longitude=-119.4,
        delivery_postal_code="V1V 1V1"
    )
    
    result = service.create_order(payload)

    # Asserting directly on the returned object
    assert result.customer_id == "brady_123"
    assert len(result.items) == 1
    mock_repo.save_all.assert_called_once()

def test_create_order_invalid_data_handling(service):
    """
    Fault Injection / Exception Handling
    Ensure HTTPException is raised when validation fails
    """
    payload = OrderCreate(
        customer_id="brady_123",
        restaurant_id=1,
        items=[],
        delivery_latitude=150.0, # Invalid
        delivery_longitude=-119.4,
        delivery_postal_code="V1V 1V1"
    )
    with pytest.raises(HTTPException) as exc:
        service.create_order(payload)

    assert exc.value.status_code == 400

# --- Update Order Tests ---

def test_update_order_status_success(service, mock_repo):
    """
    Functional Test
    Ensure order status can be updated
    """
    existing_order = {
        "id": "abc123A",
        "customer_id": "brady_1",
        "restaurant_id": 1,                    
        "status": OrderStatus.UNPAID,
        "delivery_latitude": 49.8,              
        "delivery_longitude": -119.4,          
        "delivery_postal_code": "V1V 1V1",      
        "order_date": "2026-03-25T12:00:00",    
        "cost_breakdown": 0,                    
        "items": []
    }
    mock_repo.load_all.return_value = [existing_order]
    
    update_data = MagicMock()
    update_data.status = OrderStatus.PENDING
    update_data.delivery_latitude = None
    update_data.delivery_longitude = None
    update_data.delivery_postal_code = None

    result = service.update_order("abc123A", update_data)

    assert result.status == OrderStatus.PENDING
    mock_repo.save_all.assert_called_once()

def test_update_order_not_found(service, mock_repo):
    """
    Equivalence Partitioning
    Test updating an order that doesn't exist
    """
    mock_repo.load_all.return_value = []
    
    with pytest.raises(HTTPException) as exc:
        service.update_order("fake_id", MagicMock())

    assert exc.value.status_code == 404
    assert exc.value.detail == "Order not found"