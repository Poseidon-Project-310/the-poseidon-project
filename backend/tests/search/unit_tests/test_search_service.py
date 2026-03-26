# backend/tests/search/unit_tests/search_service.py
import pytest
from unittest.mock import MagicMock
from backend.services.search_service import SearchService


def test_search_returns_empty_for_short_query(search_service):
    # Feat3-FR2
    # Boundary value analysis: If a search is only one letter and they
    # Try to search, nothing will show up to save resources
    assert search_service.search_by_keyword("") == []
    assert search_service.search_by_keyword("a") == []
    assert search_service.search_by_keyword("  ") == []

def test_search_by_keyword_success(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Functional Logic
    Tests that a valid keyword returns matching items from published restaurants.
    """
    mock_res = MagicMock()
    mock_res.id = 10
    mock_res.is_published = True
    mock_restaurant_repo.load_all.return_value = [mock_res]

    mock_item = MagicMock()
    mock_item.restaurant_id = 10
    mock_item.name = "Beef Pie"
    mock_item.tags = ["savory"]
    mock_item.model_dump.return_value = {"item_name": "Beef Pie", "tags": ["savory"]}
    
    mock_item_repo.load_all.return_value = [mock_item]

    results = search_service.search_by_keyword("beef")

    assert len(results) == 1
    assert results[0]["item_name"] == "Beef Pie"


def test_search_filters_unpublished_restaurants(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Equivalence Partitioning
    Items should NOT appear in search if their restaurant is not published.
    """
    mock_res = MagicMock(id=10, is_published=False)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    mock_item = MagicMock(restaurant_id=10, name="Hidden Pizza", tags=[])
    mock_item_repo.load_all.return_value = [mock_item]

    results = search_service.search_by_keyword("pizza")

    assert len(results) == 0


def test_search_by_tag_match(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Functional Test
    Tests that searching for a tag (e.g., 'vegan') returns the item.
    """
    mock_res = MagicMock(id=1, is_published=True)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    mock_item = MagicMock()
    mock_item.restaurant_id = 1
    mock_item.name = "Salad"
    mock_item.tags = ["vegan", "healthy"]
    mock_item.model_dump.return_value = {"item_name": "Salad", "tags": ["vegan"]}
    
    mock_item_repo.load_all.return_value = [mock_item]

    results = search_service.search_by_keyword("vegan")

    assert len(results) == 1
    assert "Salad" in results[0]["item_name"]


def test_get_homepage_featured_limit(search_service, mock_restaurant_repo, mock_item_repo):
    """
    Functional test
    Ensures only the first 5 published items are returned.
    """
    mock_res = MagicMock(id=1, is_published=True)
    mock_restaurant_repo.load_all.return_value = [mock_res]

    items = []
    for i in range(10):
        item = MagicMock(restaurant_id=1)
        item.model_dump.return_value = {"id": i}
        items.append(item)
    
    mock_item_repo.load_all.return_value = items

    featured = search_service.get_homepage_featured()

    assert len(featured) == 5
