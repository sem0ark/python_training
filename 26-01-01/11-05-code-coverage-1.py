import pytest

# ===============================================================
# The code to cover with tests
# ===============================================================


class Config:
    """
    A configuration manager for the Reluctant Cloud Controller.

    Requirements:
    1. Store arbitrary key-value pairs in a 'data' dictionary.
    2. Provide a 'begin_transaction' method returning a context manager.
    3. If the context block succeeds, changes to 'data' are committed.
    4. If the context block raises an exception, 'data' reverts to its pre-entry state.
    5. All exceptions raised within the block must be propagated (re-raised).
    6. Rollback must correctly handle added, modified, and deleted keys.
    """

    def __init__(self, **initial_data):
        self.data = initial_data

    def begin_transaction(self):
        if not isinstance(self.data, dict):
            # This handles cases where 'data' might have been corrupted externally
            raise TypeError("Configuration data must be a dictionary.")
        return Transaction(self)


class Transaction:
    def __init__(self, owner):
        self.owner = owner
        self._snapshot = None

    def __enter__(self):
        # Create a shallow copy to track key/value changes in the dictionary
        self._snapshot = self.owner.data.copy()
        return self.owner

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Revert the owner's data to the state captured at __enter__
            self.owner.data = self._snapshot
            return False  # Propagate the exception

        # Explicitly return True to mark a successful branch in coverage
        return True


# ===============================================================
# TESTS
# ===============================================================


class TestAtomicConfig:
    """
    Goal: Reach 100% branch coverage for the Config and Transaction classes.
    """

    def test_transaction_commit(self):
        """Verify changes persist after a successful transaction."""
        conf = Config(region="us-east-1", retries=3)
        with conf.begin_transaction():
            conf.data["region"] = "eu-central-1"
            conf.data["timeout"] = 30

        assert conf.data["region"] == "eu-central-1"
        assert conf.data["timeout"] == 30

    # TODO: Implement additional tests to reach 100% coverage.
    # Consider the following scenarios:
    # - What happens if an exception is raised inside the 'with' block? (Rollback check)
    # - Does the exception actually reach the caller? (Propagation check)
    # - Are deleted keys restored during a rollback?
    # - Are newly added keys removed during a rollback?
    # - What happens if 'conf.data' is not a dictionary when 'begin_transaction' is called?


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - To test the exception branch in __exit__, you must use `pytest.raises` around the `with` block.
# - Ensure you test all three dictionary operations: adding a new key, modifying an existing key, and deleting a key.
# - The `TypeError` in `begin_transaction` requires a test where `conf.data` is manually set to something else (like None).
# - Remember that the context manager's `__exit__` returns `False` to propagate exceptions; your tests must verify both the rollback AND the fact that the exception was re-raised.
