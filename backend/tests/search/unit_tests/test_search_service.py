# backend/tests/search/unit_tests/test_search_service.py
import pytest
from backend.services.search_service import SearchService
from backend.models.restaurant.restaurant_model import Restaurant
from backend.repositories.restaurant_repository import RestaurantRepository


@pytest.fixture
def mock_db():
    """Provides a fresh list to act as the database for each test."""
    return []

@pytest.fixture
def restaurant_repo(mock_db):
    """Initializes the repo with the mock database."""
    return RestaurantRepository(mock_db)


@pytest.fixture
def search_service(restaurant_repo):
    """Initializes the service with the mock repository."""
    return SearchService(restaurant_repo)


@pytest.fixture
def owner():
    class Owner:
        id = 1
    return Owner()


@pytest.fixture
def published_restaurant(owner):
    """Returns a restaurant model already set to published."""
    return Restaurant(
        name="Published Cafe",
        owner=owner,
        is_published=True,
        address="123 Main St",
        phone="555-0123",
        open_time=900,
        close_time=2100
    )


@pytest.fixture
def draft_restaurant(owner):
    """Returns a restaurant model that is not yet published."""
    return Restaurant(
        name="Draft Diner",
        owner=owner,
        is_published=False
    )

# --- Search and browse ---

def test_browse_homepage_returns_only_published(
        search_service, restaurant_repo,
        published_restaurant, draft_restaurant):
    """
    Feat3-FR3: 
    Functional Test User can open a restaurant's menu from the homepage.
    """
    restaurant_repo.create_restaurant(published_restaurant)
    restaurant_repo.create_restaurant(draft_restaurant)

    results = search_service.browse_homepage()

    assert len(results) == 1
    assert results[0]["name"] == "Published Cafe"
    assert "average_rating" in results[0],f"Missing rating! Keys: {results[0].keys()}"
    assert "id" in results[0]


def test_get_restaurant_details_success(
        search_service, restaurant_repo, published_restaurant):
    """
    Feat3-FR3:
    Functional test: Customer reviews are visible to users.
    Verification: Opening a restaurant returns the full
    dictionary including menu and reviews.
    """
    res_id = restaurant_repo.create_restaurant(published_restaurant)

    details = search_service.get_restaurant_details(res_id)

    assert details is not None
    assert details["name"] == "Published Cafe"
    assert "menu" in details
    assert "reviews" in details
    assert isinstance(details["reviews"], list)


# --- Edge Case Tests ---

def test_get_restaurant_details_blocks_unpublished(
        search_service, restaurant_repo, draft_restaurant):
    """
    Feat3-FR3:
    Edge Case: Ensure that even if we have the ID,
    we cannot 'open' a draft restaurant.
    """
    res_id = restaurant_repo.create_restaurant(draft_restaurant)

    details = search_service.get_restaurant_details(res_id)

    assert details is None


def test_get_details_nonexistent_id(search_service):
    """
    Feat3-FR3:
    Edge Case: Verify that an invalid ID returns None
    instead of crashing.
    """
    details = search_service.get_restaurant_details(9999)
    assert details is None


def test_homepage_empty_state(search_service, restaurant_repo):
    """
    Feat3-FR3:
    Edge Case: Verify homepage doesn't crash if no
    restaurants are published.
    """
    results = search_service.browse_homepage()
    assert results == []
