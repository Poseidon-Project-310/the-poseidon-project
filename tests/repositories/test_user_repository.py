#testing for user repository
import json
from pathlib import Path
import pytest

from backend.repositories import user_repository

@pytest.fixture
def repo(tmp_path):
    user_repository.DATA_FILE = tmp_path / "users.json"  
    return user_repository.UserRepository()

def test_create(repo):
    user_data = {
        "username": "anjana",
        "id": 1,
        "email": "anjanaoned@gmail.com" }
    created_user = repo.create(user_data)
    assert created_user["id"] == 1
    assert created_user["username"] == "anjana"

def test_find_by_username(repo):
    user_data = {
        "username": "anjana",
        "id": 1,
        "email": "anjanaoned@gmail.com" }
    repo.create(user_data)
    found_user = repo.find_by_username("anjana")
    assert found_user["username"] == "anjana"
    assert found_user["id"] == 1

def test_find_by_id(repo):
    user_data = {
        "username": "anjana",
        "id": 1,
        "email": "anjanaoned@gmail.com" }
    repo.create(user_data)  
    found_user = repo.find_by_id(1)
    assert found_user["username"] == "anjana"   
    assert found_user["id"] == 1

def test_find_missing_returns_none(repo):
    assert repo.find_by_username("nope") is None
    assert repo.find_by_id(999) is None