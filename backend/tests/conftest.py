# backend/tests/conftest.py
import pytest
import sys
from pathlib import Path
from decimal import Decimal
from uuid import uuid4
from unittest.mock import MagicMock
from backend.schemas.items_schema import MenuItem as MenuItemSchema



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

