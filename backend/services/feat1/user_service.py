from __future__ import annotations

# this file handles user-related business logic
# it works between the route/controller layer and  repository layer
# the service is responsible for things like checking for duplicate usernames,
# hashing passwords, creating users, and saving them using the repository

import bcrypt
from dataclasses import asdict

from backend.models.user.user_model import User
from backend.repositories.user_repository import UserRepository


class UserService:
    """
    user Service
    this service handles the main user business logic.

    old setup:
      - checked user role
      - created Customer / Admin / RestaurantOwner objects
      - used repository methods like find_by_username() and create()
      - used model methods like hash_password(), to_dict(), and from_dict()

    new setup:
      - uses only one merged user mode
      - loads all users from the repository
      - checks for duplicate usernames in the service
      - hashes passwords in the service
      - generates new ids in the service
      - saves updated user data using the repository
      - returns User objects from the serviceq

    why we changed this:
      - the repository should only load/save data (as team mentioned)
      - the model should only describe the user structure
      - the service should contain the business logic
    """

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def hash_password(self, password: str) -> str:
        """
        take a plain text password and return a hashed version of it.
        we store the hash, not the original password for security reasons
        """
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def create_user(self, username: str, email: str, password: str) -> User:
        """
        create a new user if the username is not already taken.

        steps:
          - load all existing users
          - check for duplicate username
          - hash the password
          - create a new merged User object
          - save the updated user list
          - return the new user
        """
        users = self.user_repo.load_all()

        for existing_user in users:
            if existing_user["username"] == username:
                raise ValueError("username already exists")

        new_id = str(len(users) + 1)
        password_hash = self.hash_password(password)

        user = User(
            id=new_id,
            username=username,
            email=email,
            password_hash=password_hash
        )

        users.append(asdict(user))
        self.user_repo.save_all(users)

        return user