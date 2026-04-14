"""
Internal Name Mangling & Static Utility

Implement data hiding for a password and a "@staticmethod" to validate password strength without needing an instance.
"""

import pytest


class Account:
    def __init__(self, user, password):
        self.user = user
        # 1. Use double underscore to mangle the password attribute
        raise NotImplementedError()

    @staticmethod
    def is_strong(password):
        """Returns True if password is > 8 chars, else False"""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_password_mangling():
    acc = Account("dev", "secret123")
    assert not hasattr(acc, "__password")
    # Check if name mangling worked (Class name prepended)
    assert hasattr(acc, f"_{Account.__name__}__password")


def test_static_validation():
    assert Account.is_strong("123456789") is True
    assert Account.is_strong("weak") is False


def test_password_mangling_hides_attr():
    acc = Account("dev", "12345678")
    assert not hasattr(acc, "__password")


def test_mangled_access_via_dir():
    acc = Account("dev", "secret")
    # Verify the specific mangled name pattern: _ClassName__attr
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
