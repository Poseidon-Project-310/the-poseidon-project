# backend/tests/restaurant/unit_tests/test_restaurant_schema.py
import pytest
from pydantic import ValidationError
from backend.schemas.restaurant_schema import RestaurantSchema

@pytest.fixture
def base_data():
    return{
        "_id": "res_123",
        "_name": "Testaurant",
        "_menu": ["Burger", "Fries"],
        "_open_time": 900,
        "_close_time": 2200,
        "_latitude": 49.2827,
        "_longitude": -123.1207,
        "_is_published": False
    }

def test_restaurant_schema_initialization(base_data):
    """
    Equivalence Partitioning
    Maps the valid data from the fixture to the private attributes
    """
    restaurant = RestaurantSchema(**base_data)

    assert restaurant.restaurant_id == "res_123"
    assert restaurant.name == "Testaurant"
    assert restaurant.get_open_time == 900


def test_restaurant_optional_fields_null(base_data):
    """
    Equivalence Partitioning
    Test that optional tests when not filled out doesn't cause an error
    """
    restaurant = RestaurantSchema(**base_data)
    assert restaurant._address is None
    assert restaurant._phone is None


def test_restaurant_encapsulation_boundaries(base_data):
    """
    Fault Injection
    Tries to access a protected attribute
    """
    restaurant = RestaurantSchema(**base_data)

    public_data = restaurant.model_dump()
    assert "_id" not in public_data
    assert "_name" not in public_data

    with pytest.raises(AttributeError):
        _ = restaurant.some.non_existing_field
    

def test_restaurant_invalid_time_logic(base_data):
    """
    Exception Handling
    Tests handling invalid data and throws errors through setters
    """
    restaurant = RestaurantSchema(**base_data)

    with pytest.raises(ValueError, match="Invalid time format"):
        restaurant.get_open_time = 9999


def test_restaurant_invalid_time_relationship(base_data):
    """
    Exception Handling
    Ensures that open_time cannot be after or equal to close_time
    """
    base_data["_open_time"] = 2200
    base_data["_close_time"] = 900

    with pytest.raises(ValidationError) as exc_info:
        RestaurantSchema(**base_data)

    assert "open_time must be before close_time" in str(exc_info.value)


def test_restaurant_serialization_mock(base_data):
    """
    Mocking
    Testing saving through the repository
    """
    restaurant = RestaurantSchema(**base_data)
    mock_save_data = restaurant.model_dump(by_alias=True, exclude_none=True)

    assert "_id" in mock_save_data
    assert "_name" in mock_save_data
    assert mock_save_data["_id"] == "res_123"


def test_restaurant_status_update(base_data):
    """
    Positive Functional Test
    Test of data flow to publish restaurant
    """
    restaurant = RestaurantSchema(**base_data)
    assert restaurant.is_published is False

    restaurant.is_published = True
    assert restaurant.is_published is True

def test_restaurant_attr_to_private_mapping():
    """
    Functional Test
    Match the public fields to post_init
    """
    input_data = {
        "res_id_attr": "res_123",
        "name_attr": "Testaurant",
        "open_time_attr": 900,
        "is_published_attr": True
    }
    restaurant = RestaurantSchema(**input_data)

    assert restaurant._id == "res_123"
    assert restaurant.restaurant_id == "res_123"
    assert restaurant._is_published is True