# backend/tests/restaurant/unit_tests/test_menu_item_model.py
import pytest
from backend.models.restaurant.menu_item_model import MenuItem


def test_menu_item_initialization():
    """
    Positive Functional Test: Verify a MenuItem can be created
    """
    item = MenuItem(name="Tacos", price=10.50, restaurant_id=1)

    assert item.name == "Tacos"
    assert item.price == 10.50
    assert item.restaurant_id == 1
    assert item.id is None  # Confirms our Optional[int] = None update


def test_menu_item_missing_restaurant_id():
    """
    Negative Edge Case: A menu item must belong to a restaurant
    """
    with pytest.raises(TypeError):
        # Missing the mandatory restaurant_id argument
        MenuItem(name="Ghost Burger", price=5.00)


def test_menu_item_price_edge_cases():
    """
    Edge Case: Testing zero-price and high-price items
    """
    free_item = MenuItem(name="Free Water", price=0.0, restaurant_id=1)
    expensive_item = MenuItem(name="Gold Pizza", price=999.99, restaurant_id=1)

    assert free_item.price == 0.0
    assert expensive_item.price == 999.99


def test_menu_item_equality():
    """
    Functional Test: Two items with
    the same data should be equal.
    """
    item1 = MenuItem(name="Coffee", price=3.50, restaurant_id=2)
    item2 = MenuItem(name="Coffee", price=3.50, restaurant_id=2)

    assert item1 == item2
