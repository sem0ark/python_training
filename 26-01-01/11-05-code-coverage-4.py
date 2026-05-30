import pytest

# ===============================================================
# The code to cover
# ===============================================================


class MissingSchemaError(Exception):
    """Raised when the mandatory schema_version key is absent."""

    pass


class PayloadProcessingError(Exception):
    """Raised when internal processing fails due to low-level data errors."""

    pass


def process_payload(data):
    """
    Processes a data payload and wraps low-level errors for business logic.

    Requirements:
    1. Raise MissingSchemaError if 'schema_version' is not in the data dictionary.
    2. Catch KeyError, TypeError, or ValueError during processing.
    3. Wrap caught errors in a PayloadProcessingError.
    4. The PayloadProcessingError message must include the original error's class name.
    5. The original error must be set as the direct cause (__cause__).
    """
    if "schema_version" not in data:
        raise MissingSchemaError(
            "Payload is missing the required 'schema_version' key."
        )

    try:
        # Simulated processing logic
        version = data["schema_version"]
        entries = data["entries"]
        # This line can trigger TypeError (if entries not iterable)
        # or ValueError (if strings aren't numeric)
        total = sum(float(x) for x in entries)

        return {"version": version, "count": len(entries), "total": total}
    except (KeyError, TypeError, ValueError) as e:
        error_name = type(e).__name__
        message = f"Processing failed due to an underlying {error_name}"
        raise PayloadProcessingError(message) from e


# ===============================================================
# TESTS
# ===============================================================


class TestDataPipeline:
    """
    Goal: Reach 100% branch coverage for the process_payload function.
    """

    def test_process_success(self):
        """Verify successful processing returns the expected summary."""
        payload = {"schema_version": "1.0", "entries": ["10.5", "20", "5.5"]}
        result = process_payload(payload)
        assert result["total"] == 36.0
        assert result["count"] == 3

    # TODO: Add more tests below to reach 100% coverage:
    # - Missing schema: Verify MissingSchemaError is raised.
    # - Missing entries: Verify PayloadProcessingError is raised from a KeyError.
    # - Invalid entry types: Verify PayloadProcessingError is raised from a TypeError.
    # - Non-numeric entries: Verify PayloadProcessingError is raised from a ValueError.
    # - Chaining: Verify the __cause__ attribute of PayloadProcessingError is the original exception.
    # - Message: Verify the PayloadProcessingError message contains the original exception name.


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - Use `exc_info.value.__cause__` to inspect the exception that triggered the current one.
# - To trigger a TypeError, pass something that isn't a list to "entries".
# - To trigger a ValueError, pass a list of strings that cannot be converted to floats (e.g., ["abc"]).
# - To trigger a KeyError, provide a dictionary with "schema_version" but without "entries".
# - Exception chaining using `raise ... from e` is what populates the `__cause__` attribute.
