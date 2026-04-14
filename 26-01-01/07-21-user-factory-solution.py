"""
Multi-Format User Factory
Use "@classmethod" to create a "User" object from different data sources (JSON-like dicts or raw strings).
"""

import pytest


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

    @classmethod
    def from_dict(cls, data):
        """Creates a User from a dictionary {'name': '...', 'email': '...'}"""
        return cls(username=data["name"], email=data["email"])

    @classmethod
    def from_string(cls, raw_str):
        """Creates a User from a string 'username:email'"""
        args = raw_str.split(":")
        if len(args) != 2:
            raise ValueError("Input string must be in the format 'username:email'")
        return cls(*args)


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_factories():
    u1 = User.from_dict({"name": "alice", "email": "a@test.com"})
    u2 = User.from_string("bob:b@test.com")

    assert u1.username == "alice"
    assert u2.email == "b@test.com"
    assert isinstance(u1, User)


def test_factory_from_dict():
    u = User.from_dict({"name": "bob", "email": "b@b.com"})
    assert u.username == "bob"


def test_factory_from_string():
    u = User.from_string("alice:a@a.com")
    assert u.email == "a@a.com"


def test_factory_invalid_string():
    with pytest.raises(ValueError):
        User.from_string("invalid_format_no_colon")


def test_factory_is_instance():
    u = User.from_string("test:test@test.com")
    assert isinstance(u, User)


def test_factory_dict_missing_key():
    with pytest.raises(KeyError):
        User.from_dict({"only_name": "mark"})


if __name__ == "__main__":
    pytest.main([__file__])
