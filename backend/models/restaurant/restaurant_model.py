# backend/models/restaurant/restaurant_model.py

import uuid

# Typing used for type hints to avoid circular imports
from typing import TYPE_CHECKING, List

# Read by VSCode for type checking but python ignores
if TYPE_CHECKING:
    from backend.models.user.restaurant_owner_model import RestaurantOwner
    from backend.models.restaurant.menu_item_model import MenuItem


# Restaurant information
class Restaurant:
    def __init__(self, name: str, owner: "RestaurantOwner", **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        self.name = name
        self.owner = owner

        # Set all kwargs as attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

        # Status
        self.is_open: bool = False

        # Menu
        self.menu: List["MenuItem"] = []

        # Reviews
        self.reviews: List = []
        self.total_reviews: int
    
    def total_reviews(self) -> int:
        return len(self.reviews)

    def get_average_rating(self) -> float:
        if not self.reviews:
            return 0.0
        average = sum(review.rating for review in self.reviews
                      ) / len(self.reviews)
        return round(average, 1)
