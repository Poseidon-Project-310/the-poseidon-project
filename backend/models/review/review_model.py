# backend/models/review/review_model.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Review:
    rating: int
    restaurant_id: int
    customer_name: str
    comment: str
    customer_id: int
    id: Optional[int] = None
