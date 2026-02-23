from typing import List
from dataclasses import field
from datetime import time
from enum import Enum

# Read by VSCode for type checking but python ignores
if TYPE_CHECKING:
    from backend.models.user.restaurant_owner_model import RestaurantOwner
    from backend.models.restaurant.menu_item_model import MenuItem


# Enum for days of the week
# Allows easy ref to days consistently
class DayOfWeek(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

# Business hours for a restaurant
class BusinessHours:
    day: DayOfWeek
    open_time: time
    close_time: time
    is_closed: bool = False

# Restaurant information
class Restaurant:
    def __init__(self, id: int, name: str, owner: "RestaurantOwner"):
        self.id = id
        self.name = name
        self.owner = owner

        # Operational details
        self.address = ""
        self.city = ""
        self.postal_code = ""
        self.phone = ""
        self.cuisine_type = ""
        self.business_hours = []
        self.open_time = None
        self.close_time = None
        self.rating = 0.0
        self.total_reviews = 0
        self.reviews = [] # new list created so no duplicates
        # Status
        self.is_open = False

        # Menu
        self.menu = []

    # getter
    def get_menu(self) -> List[MenuItem]:
        return self.menu
    # method to calculate average rating
    def get_average_rating(self) -> float:
        if self.total_reviews == 0:
            return 0.0
        return sum(review.rating for review in self.reviews) / self.total_reviews
    
    def is_open(self) -> bool:
        # Check if restaurant is currently open
        # implementation would check current time against business hours
        pass
