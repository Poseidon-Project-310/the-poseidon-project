# backend/models/user/init.user.py
#this file defines a user class, it represnets users within our system (customers, restaurant owners, admins).

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Dict

from backend.models.user.roles import ALL_ROLES, CUSTOMER


@dataclass
class User:
    """
    User Model (based on UML diagram)

    UML Attributes:
      - id: int
      - username: String
      - password: String

    In our code:
      - we stored password_hash instead of raw password for safety, as hashing is a one way function and it is unsafe to store raw passwords.
        hashing takes a raw password and converts it into a fized length of random string, and we can check if raw password is correct by hash matching.
      - we also include role (customer/admin/restaurant_owner) so we can represent
        Admin + RestaurantOwner + Customer without needing 3 separate classes yet.
    """

    id: int
    username: str
    password_hash: str
    role: str = CUSTOMER  # default role is customer

    def __post_init__(self) -> None:
        """
        This runs right after the dataclass constructor, which means it runs after we create a User object.
        We use it to validate that the User object is not invalid.
        """
        if not isinstance(self.id, int) or self.id < 0:
            raise ValueError("id must be a non-negative integer")

        if not isinstance(self.username, str) or not self.username.strip():
            raise ValueError("username must be a non-empty string")

        if not isinstance(self.password_hash, str) or not self.password_hash.strip():
            raise ValueError("password_hash must be a non-empty string")

        if self.role not in ALL_ROLES:
            raise ValueError(f"role must be one of {ALL_ROLES}")

    
    # -----------------------------------------------------------------------------
    # Password helpers
    # -----------------------------------------------------------------------------
    @staticmethod
    def hash_password(raw_password: str) -> str:
        """
        Convert a raw password into a hash string.
        (We use SHA-256 because it's simple for a course project.)
        SHA-256 is one wya function, meaning you cna convert raw password to hash, 
        but you cannot convert hash back to raw password.
        """
        if not isinstance(raw_password, str) or not raw_password:
            raise ValueError("password must be a non-empty string") 
        """this means that password must be a non-empty string, and if not we will raise an error."""
        return hashlib.sha256(raw_password.encode("utf-8")).hexdigest() 

    def check_password(self, raw_password: str) -> bool:
        """Return True if the raw password matches our stored password_hash.""" 
        return self.password_hash == User.hash_password(raw_password)

    # -----------------------------------------------------------------------------
    # UML method: login() : bool
    # -----------------------------------------------------------------------------
    def login(self, raw_password: str) -> bool:
        """
        UML says: login() -> bool
        in backend terms this means to verify the password and return True/False.
        
        """
        return self.check_password(raw_password)

    # -----------------------------------------------------------------------------
    # Repo helpers (saving/loading)
    # -----------------------------------------------------------------------------
    def to_dict(self) -> Dict:
        """Convert User into a dictionary (easy to save to JSON later)."""
        return {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role,
        }

    @staticmethod
    def from_dict(data: Dict) -> "User":
        """Create a User object from a dictionary (loaded from JSON)."""
        return User(
            id=int(data["id"]),
            username=str(data["username"]),
            password_hash=str(data["password_hash"]),
            role=str(data.get("role", CUSTOMER)),
        )

