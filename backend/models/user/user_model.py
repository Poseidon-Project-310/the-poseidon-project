# backend/models/user/user_model.py
# this file defines one merged User class.
# instead of having separate admin / customer / restaurant owner models,
# we now store all user information in one single user model.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class User:
    id: str
    username: str
    email: str
    password_hash: str
    phone: str = ""
    address: str = ""
    location: str = ""
    postal_code: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    cart: List[str] = field(default_factory=list)
    orders: List[str] = field(default_factory=list)
    owned_restaurants_id: List[str] = field(default_factory=list)

    """
    User Model (merged user version)

    this model represents every user in the system using one class only.

    old setup:
      - User
      - Customer
      - RestaurantOwner
      - Admin

    new setup:
      - only one User class

    why we changed this:
      - it keeps the architecture simpler
      - it matches the updated project structure
      - it removes the need for subclass conversion when loading JSON
      - restaurant ownership can now be tracked using owned_restaurants_id

    important notes:
      - id is now a string, not an int
      - password_hash is stored, not the raw password
      - password hashing/checking should happen in the service layer
      - JSON saving/loading should happen in the repository layer
      - this model should mainly describe the shape of a user
        and validate that the data is valid
    """

    def __post_init__(self) -> None:
        """
        this runs right after the dataclass constructor,
        so it runs immediately after we create a User object.

        we use it to validate the fields and make sure
        the object is not created with invalid data.
        """

        if not isinstance(self.id, str) or not self.id.strip():
            raise ValueError("id must be a non-empty string")

        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("username must be a non-empty string")

        if not isinstance(self.email, str) or not self.email.strip():
            raise ValueError("email must be a non-empty string")

        if "@" not in self.email:
            raise ValueError("email must contain '@'")

        if "." not in self.email.split("@", 1)[1]:
            raise ValueError("email domain must contain '.'")

        if not isinstance(self.password_hash, str) or not self.password_hash.strip():
            raise ValueError("password_hash must be a non-empty string")

        if not isinstance(self.phone, str):
            raise ValueError("phone must be a string")

        if not isinstance(self.address, str):
            raise ValueError("address must be a string")

        if not isinstance(self.location, str):
            raise ValueError("location must be a string")

        if not isinstance(self.postal_code, str):
            raise ValueError("postal_code must be a string")

        if self.latitude is not None and not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number or None")

        if self.longitude is not None and not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number or None")

        if not isinstance(self.cart, list):
            raise ValueError("cart must be a list")

        if not isinstance(self.orders, list):
            raise ValueError("orders must be a list")

        if not isinstance(self.owned_restaurants_id, list):
            raise ValueError("owned_restaurants_id must be a list")