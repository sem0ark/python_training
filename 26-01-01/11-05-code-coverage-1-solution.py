import pytest

# ===============================================================
# The code to cover with tests
# ===============================================================


class Config:
    """
    A configuration manager for the Reluctant Cloud Controller.
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

    def test_transaction_rollback_exception(self):
        """Verify changes are rolled back when an exception occurs."""
        conf = Config(region="us-east-1")
        with pytest.raises(ValueError):
            with conf.begin_transaction():
                conf.data["region"] = "eu-west-1"
                raise ValueError("Fail")

        assert conf.data["region"] == "us-east-1"

    def test_rollback_handles_add_delete(self):
        """Verify added and deleted keys are restored on rollback."""
        conf = Config(k1="v1")
        with pytest.raises(RuntimeError):
            with conf.begin_transaction():
                conf.data["k2"] = "v2"
                del conf.data["k1"]
                raise RuntimeError("Fail")

        assert conf.data == {"k1": "v1"}
        assert "k2" not in conf.data

    def test_begin_transaction_invalid_data_type(self):
        """Verify TypeError when data is not a dictionary."""
        conf = Config()
        conf.data = ["not", "a", "dict"]
        with pytest.raises(TypeError) as excinfo:
            conf.begin_transaction()
        assert "must be a dictionary" in str(excinfo.value)


if __name__ == "__main__":
    pytest.main([__file__])
