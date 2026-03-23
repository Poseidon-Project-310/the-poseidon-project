# backend/repositories/user_repository.py
# this file is responsible for saving and loading user data
# to and from the users JSON file.

import json
import os
from typing import List, Dict


DATA_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "users.json"
)


class UserRepository:
    """
    User Repository

    this repository handles only file storage operations
    for the users JSON file.

    old setup:
      - load all users
      - save all users
      - find users by username
      - find users by id
      - create users
      - hash passwords
      - assign ids

    new setup:
      - load all users
      - save all users

    why we changed this:
      - the repository layer should only deal with reading/writing data
      - business logic should not be inside the repository
      - password hashing/checking belongs in the service layer
      - user creation and lookup logic also belongs in the service layer

    important note:
      - this class works with raw dictionary data from users.json
      - it does not convert data into User objects
      - it does not validate business rules
    """

    def load_all(self) -> List[Dict]:
        """
        load and return all users from the JSON file.

        if the file does not exist yet, return an empty list
        so the system can treat it like an empty database.
        """
        if not os.path.exists(DATA_FILE):
            return []

        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_all(self, users: List[Dict]) -> None:
        """
        save the full list of users into the JSON file.

        this overwrites the existing file contents with the
        updated users list.
        """
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2)