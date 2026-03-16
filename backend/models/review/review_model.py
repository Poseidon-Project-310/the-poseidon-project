# backend/models/review/review_model.py
from dataclasses import dataclass
from typing import Optional

# Dummy review model to allow tests to pass

@dataclass
class Review:
    rating: int
    restaurant_id: int
    customer_id: int
    customer_name: str
    comment: str
    id: int = 0
