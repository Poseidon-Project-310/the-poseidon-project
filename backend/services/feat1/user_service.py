from __future__ import annotations

from dataclasses import asdict

import bcrypt

from backend.models.user.user_schema import User
from backend.repositories.user_repository import UserRepository


class UserService:
    """Handle user-related business logic."""

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        """Hash a plain-text password."""
        if not isinstance(password, str) or not password.strip():
            raise ValueError("password must be a non-empty string")

        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def create_user(self, username: str, email: str, password: str) -> User:
        """Create a new user if the username is unique."""
        users = self.user_repo._load_all()

        for existing_user in users:
            if existing_user["username"] == username:
                raise ValueError("username already exists")

        new_id = str(len(users) + 1)
        password_hash = self.hash_password(password)

        user = User(
            id=new_id,
            username=username,
            email=email,
            password_hash=password_hash,
        )

        users.append(asdict(user))
        self.user_repo._save_all(users)

        return user