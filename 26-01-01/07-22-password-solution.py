"""
Internal Name Mangling & Static Utility

Implement data hiding for a password and a "@staticmethod" to validate password strength without needing an instance.
"""

import pytest


class Account:
    def __init__(self, user, password):
        self.user = user
        self.__password = password

    @staticmethod
    def is_strong(password):
        """A strong password is at least 8 characters long."""
        return len(password) >= 8


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_password_mangling():
    acc = Account("dev", "secret123")
    assert not hasattr(acc, "__password")
    assert hasattr(acc, f"_{Account.__name__}__password")


def test_static_validation():
    assert Account.is_strong("123456789") is True
    assert Account.is_strong("weak") is False


def test_password_mangling_hides_attr():
    acc = Account("dev", "12345678")
    assert not hasattr(acc, "__password")


def test_mangled_access_via_dir():
    acc = Account("dev", "secret")
    assert hasattr(acc, "_Account__password")


def test_static_is_strong_true():
    assert Account.is_strong("longpassword") is True


def test_static_is_strong_false():
    assert Account.is_strong("short") is False


def test_static_is_strong_boundary():
    assert Account.is_strong("12345678") is True  # Exactly 8


def test_static_with_empty_string():
    assert Account.is_strong("") is False


if __name__ == "__main__":
    pytest.main([__file__])
