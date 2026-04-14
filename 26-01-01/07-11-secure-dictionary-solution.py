"""
"Case-Insensitive" Secure Dictionary

Goal: Create a class that stores sensitive data. It should allow key access like a dictionary but ignore case and prevent the deletion of specific protected keys.
"""

import pytest


class SecureVault:
    """
    Requirements:
    1. Implement `__setitem__` to store keys in lowercase.
    2. Implement `__getitem__` to retrieve keys regardless of case.
    3. Implement `__delitem__` to prevent deleting the key 'admin'.
       Raise a KeyError if someone tries to delete 'admin'.
    """

    def __init__(self):
        self._data = {}

    def __setitem__(self, key, value):
        self._data[key.lower()] = value

    def __getitem__(self, key):
        return self._data[key.lower()]

    def __delitem__(self, key):
        if key.lower() == "admin":
            raise KeyError("Cannot delete admin")
        del self._data[key.lower()]


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_vault_case_insensitivity():
    v = SecureVault()
    v["API_KEY"] = "12345"
    assert v["api_key"] == "12345"
    assert v["ApI_KeY"] == "12345"


def test_vault_admin_protection():
    v = SecureVault()
    v["admin"] = "root"
    with pytest.raises(KeyError, match="Cannot delete admin"):
        del v["admin"]


def test_vault_case_insensitivity():
    v = SecureVault()
    v["API_KEY"] = "12345"
    assert v["api_key"] == "12345"
    assert v["ApI_KeY"] == "12345"


def test_vault_admin_protection():
    v = SecureVault()
    v["admin"] = "root"
    with pytest.raises(KeyError, match="Cannot delete admin"):
        del v["admin"]


def test_vault_overwrite():
    v = SecureVault()
    v["Token"] = "old"
    v["TOKEN"] = "new"
    assert v["token"] == "new"
    assert len(v._data) == 1


def test_vault_missing_key():
    v = SecureVault()
    with pytest.raises(KeyError):
        _ = v["non_existent"]


def test_vault_delete_normal_key():
    v = SecureVault()
    v["guest"] = "123"
    del v["GUEST"]
    assert "guest" not in v._data


if __name__ == "__main__":
    pytest.main([__file__])
