import pytest
from backend.repositories.restaurant_repository import RestaurantRepository


# --- Fixtures ---
@pytest.fixture
def restaurant_repo():
    mock_db = []
    return RestaurantRepository(mock_db)

# --- Restaurant Information ---


def test_create_restaurant(restaurant_repo):
    # Test for Feat2-FR1: Storing information
    # Verifies data passed to repo is saved
    restaurant_data = {
        "name": "Testaurant",
        "address": "123 Test"}

    result = restaurant_repo.create_restaurant(restaurant_data)
    assert result is not None
    assert len(restaurant_repo.get_all_restaurants()) == 1


def test_update_restaurant(restaurant_repo):
    # Test for Feat2-FR3: Correct and accurate information
    # Verifies updates to restaurant data are saved
    restaurant = restaurant_repo.create_restaurant({
        "name": "Testaurant", "address": "123 Test"})

    restaurant_repo.update_restaurant(restaurant, {"address": "456 Test"})

    updated_restaurant = restaurant_repo.get_by_id(restaurant)
    assert updated_restaurant["address"] == "456 Test"
    assert updated_restaurant["name"] == "Testaurant"

# --- Browsing and Search ---


def test_search_by_cuisine(restaurant_repo):
    # Test for Feat3-FR4: Filtering search results
    # Verifies searching by cuisine returns correct results
    restaurant_repo.create_restaurant({
        "name": "Sushi Place", "cuisine": "Japanese"})
    restaurant_repo.create_restaurant({
        "name": "Pasta House", "cuisine": "Italian"})

    results = restaurant_repo.search_by_cuisine("Japanese")
    assert len(results) == 1
    assert results[0]["name"] == "Sushi Place"


def test_pagination(restaurant_repo):
    # Test for Feat3-FR5: Paginated results
    # Verifies pagination returns correct number of results
    for i in range(10):
        restaurant_repo.create_restaurant({
            "name": f"Restaurant {i}", "cuisine": "Test"})

    page1 = restaurant_repo.get_restaurants_paginated(page=1, limit=5)
    page2 = restaurant_repo.get_restaurants_paginated(page=2, limit=5)

    assert len(page1) == 5
    assert len(page2) == 5

# Edge case: Get non-existent restaurant


def test_get_nonexistent_restaurant(restaurant_repo):
    # Verifies getting a non-existent restaurant returns None
    result = restaurant_repo.get_by_id("999")
    assert result is None

# --- Search tests ---


def test_search_by_restaurant_name(restaurant_repo):
    """
    Feat3-FR2:
    Functional test: Verify search finds matches
    in the restaurant name
    """
    restaurant_repo.create_restaurant({"name": "Burger King", "menu": []})
    restaurant_repo.create_restaurant({"name": "Pizza Hut", "menu": []})

    results = restaurant_repo.search_restaurants_and_menu_items("Burger")

    assert len(results) == 1
    assert results[0]["name"] == "Burger King"


def test_search_by_menu_item_name(restaurant_repo):
    """
    Feat3-FR2:
    Functional test: Verify search finds matches deep inside
    the menu list
    """
    # Restaurant name doesn't match, but the menu does
    restaurant_repo.create_restaurant({
        "name": "The Italian Place",
        "menu": [{"name": "Pepperoni Pizza"}, {"name": "Lasagna"}]
    })

    results = restaurant_repo.search_restaurants_and_menu_items("Pizza")

    assert len(results) == 1
    assert results[0]["name"] == "The Italian Place"


def test_search_is_case_insensitive(restaurant_repo):
    """
    Feat3-FR2:
    Functional test: 'pizza' should match 'Pizza'
    """
    restaurant_repo.create_restaurant({"name": "Pizza Palace", "menu": []})

    results = restaurant_repo.search_restaurants_and_menu_items("PIZZA")

    assert len(results) == 1


def test_search_with_empty_string(restaurant_repo):
    """
    Feat3-FR2:
    Edge Case: Searching for an empty string
    should return an empty list and not everything
    """
    restaurant_repo.create_restaurant({"name": "Anywhere", "menu": []})

    assert restaurant_repo.search_restaurants_and_menu_items("") == []
    assert restaurant_repo.search_restaurants_and_menu_items("   ") == []


def test_search_with_missing_menu_key(restaurant_repo):
    """
    Feat3-FR2:
    Edge Case: Ensure search doesn't crash if a
    restaurant dict has no 'menu' key
    """
    restaurant_repo.create_restaurant({"name": "Old School Diner"})

    # This should return a result based on name without raising a KeyError
    results = restaurant_repo.search_restaurants_and_menu_items("Diner")
    assert len(results) == 1


def test_search_partial_match(restaurant_repo):
    """
    Feat3-FR2:
    Edge Case: Searching for 'zz' should find 'Pizza'.
    """
    restaurant_repo.create_restaurant({"name": "Pizza Hut", "menu": []})

    results = restaurant_repo.search_restaurants_and_menu_items("zz")
    assert len(results) == 1
