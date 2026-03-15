# backend/models/restaurant/menu_item_model.py
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class MenuItem:
    name: str
    price: float
    restaurant_id: int
    id: Optional[int] = None
