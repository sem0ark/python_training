"""
Implement a "Secure File Vault" that wraps low-level OS errors into domain-specific exceptions.
- Create a base exception VaultError
- Create a child exception AccessDeniedError
- Implement a function read_vault(path, key)
- Logic:
    - If key is not "SECRET", raise AccessDeniedError("Invalid Key") and suppress traceback context.
    - Try to open the file at path for reading.
        - If a FileNotFoundError occurs, catch it and raise VaultError("Vault not found"), make sure to preserve the original traceback for debugging.
        - If a PermissionError occurs, catch it and raise AccessDeniedError("System restriction"), make sure to preserve the original traceback for debugging.
"""

import pytest


class VaultError(...):
    pass


class AccessDeniedError(...):
    pass


def read_vault(path, key):
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_vault_invalid_key_suppression():
    """Test that security-related errors hide the original context."""
    with pytest.raises(AccessDeniedError) as exc_info:
        read_vault("any_path", "WRONG_KEY")

    assert str(exc_info.value) == "Invalid Key"
    assert exc_info.value.__cause__ is None
    assert exc_info.value.__suppress_context__ is True


def test_vault_missing_file_chaining():
    """Test that technical errors provide debugging context via chaining."""
    with pytest.raises(VaultError) as exc_info:
        read_vault("non_existent_file.txt", "SECRET")

    assert "Vault not found" in str(exc_info.value)
    assert isinstance(exc_info.value.__cause__, FileNotFoundError)


def test_vault_inheritance():
    """Verify that AccessDeniedError is a subclass of VaultError."""
    assert issubclass(AccessDeniedError, VaultError)


def test_vault_permission_error_chaining():
    """Test chaining for PermissionErrors."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(AccessDeniedError) as exc_info:
            read_vault(tmpdir, "SECRET")

        assert "System restriction" in str(exc_info.value)
        assert isinstance(
            exc_info.value.__cause__, (PermissionError, IsADirectoryError)
        )


if __name__ == "__main__":
    pytest.main([__file__])
