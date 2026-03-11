# backend/tests/restaurant/unit_tests/test_restaurant_model.py
import pytest
from backend.models.restaurant.restaurant_model import Restaurant
from unittest.mock import MagicMock


# FR1/ FR2: Initialization tests

def test_restaurant_initialization(mock_owner):
    # Ensure restaurant initializes correctly with valid data
    restaurant = Restaurant(name="Testaurant", owner=mock_owner)
    assert restaurant.name == "Testaurant"
    assert restaurant.is_published is False
    assert isinstance(restaurant.id, str)

# FR3: Validation tests

def test_validate_for_publish_success(mock_owner):
    # Positive functional test: Valid restaurant should pass validation
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time=900,
        close_time=2100
    )
    restaurant.validate_for_publish()
    
def test_validate_for_publish_missing_field(mock_owner):
    # Negative functional test: Should not pass if missing a field
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        phone="123-456-7890",
        open_time=900,
        close_time=2100
        # address missing
    )
    with pytest.raises(ValueError, match="'address' is required"):
        restaurant.validate_for_publish()

def test_validate_for_publish_invalid_types(mock_owner):
    # Negative functional test: Should not pass if type check fails
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time="900",
        close_time=2100
    )
    with pytest.raises(ValueError, match="must be numbers"):
        restaurant.validate_for_publish()

def test_validate_for_publish_logic_error(mock_owner):
    # Negative funtional test: Should not pass if logic check fails
    restaurant = Restaurant(
        name="Testaurant",
        owner=mock_owner,
        address="123 Test St",
        phone="123-456-7890",
        open_time=2200,
        close_time=2100
    )
    with pytest.raises(ValueError, match="must be after 'close_time'"):
        restaurant.validate_for_publish()
