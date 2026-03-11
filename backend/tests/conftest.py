# backend/tests/conftest.py
import pytest
from unittest.mock import MagicMock
from backend.models.user.restaurant_owner_model import RestaurantOwner

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
def restaurant(owner):
    """
    Return default instance linked to owner
    """
    return owner.create_restaurant("John's Diner")
