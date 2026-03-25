# backend/tests/conftest.py
import pytest
import sys
from pathlib import Path
from decimal import Decimal
from uuid import uuid4
from unittest.mock import MagicMock
from backend.schemas.items_schema import MenuItem as MenuItemSchema
from backend.models.user.restaurant_owner_model import RestaurantOwner
from backend.models.restaurant.restaurant_model import Restaurant
from backend.models.restaurant.menu_item_model import MenuItem

# add project root to import path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

@pytest.fixture
def raw_menu_item_data():
    return {
        "item_name": "Beef Pie",
        "restaurant_id": 10,
        "price": "12.50",
        "id": str(uuid4())
    }

@pytest.fixture
def sample_menu_item(raw_menu_item_data):
    return MenuItemSchema(**raw_menu_item_data)

@pytest.fixture
def owner():
    """
    Return real RestaurantOwner
    """
    return RestaurantOwner(
        id=1,
        username="John_Doe",
        email="john_doe@gmail.com",
        password_hash="SecurePass123"
    )

@pytest.fixture
def mock_owner():
    """
    Return mock for tests where owner login is not important
    """
    mock = MagicMock(spec=RestaurantOwner)
    mock.id = 99
    mock.username = "MockUser"
    return mock

@pytest.fixture
def sample_item():
    """
    return valid menu item for FR3
    """
    return MenuItem(
        id=101,
        name="Burger",
        price=9.99,
        tags=["Popular"])

@pytest.fixture
def restaurant(owner, sample_item):
    """
    Return default instance linked to owner
    """
    return Restaurant(
        id=1,
        name="John's Diner",
        owner=owner,
        menu=[sample_item]
    )
