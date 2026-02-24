import os
import sys
import pytest

# Make sure project root is on path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.models.user.user_model import User
from backend.models.user.admin import Admin


def test_admin_valid_creation():
    """Admin can be created without errors and is a User subclass."""
    a = Admin(id=1, username="admin1", password_hash=User.hash_password("pw"))
    assert a.id == 1
    assert a.username == "admin1"
    assert isinstance(a, User)


def test_admin_to_dict_includes_user_type_admin():
    """Admin serialization should include user_type='Admin'."""
    a = Admin(id=2, username="admin2", password_hash=User.hash_password("pw"))
    d = a.to_dict()

    assert "user_type" in d
    assert d["user_type"] == "Admin"


def test_user_from_dict_recreates_admin():
    """
    1) Create Admin
    2) to_dict()
    3) User.from_dict()
    4) Should return Admin again
    """
    a1 = Admin(id=3, username="admin3", password_hash=User.hash_password("pw"))
    data = a1.to_dict()

    a2 = User.from_dict(data)

    assert isinstance(a2, Admin)
    assert a2.id == a1.id
    assert a2.username == a1.username
    assert a2.password_hash == a1.password_hash