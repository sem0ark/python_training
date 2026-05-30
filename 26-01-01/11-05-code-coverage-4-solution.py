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

    def test_missing_schema_version(self):
        """Verify MissingSchemaError when key is absent."""
        payload = {"entries": [1, 2]}
        with pytest.raises(MissingSchemaError) as excinfo:
            process_payload(payload)
        assert "missing the required 'schema_version' key" in str(excinfo.value)

    def test_missing_entries_error(self):
        """Verify PayloadProcessingError when 'entries' key is missing (KeyError)."""
        payload = {"schema_version": "1.0"}
        with pytest.raises(PayloadProcessingError) as excinfo:
            process_payload(payload)
        assert "underlying KeyError" in str(excinfo.value)
        assert isinstance(excinfo.value.__cause__, KeyError)

    def test_invalid_entries_type_error(self):
        """Verify PayloadProcessingError when entries is not iterable (TypeError)."""
        payload = {"schema_version": "1.0", "entries": None}
        with pytest.raises(PayloadProcessingError) as excinfo:
            process_payload(payload)
        assert "underlying TypeError" in str(excinfo.value)
        assert isinstance(excinfo.value.__cause__, TypeError)

    def test_non_numeric_entries_value_error(self):
        """Verify PayloadProcessingError when conversion fails (ValueError)."""
        payload = {"schema_version": "1.0", "entries": ["1.0", "abc"]}
        with pytest.raises(PayloadProcessingError) as excinfo:
            process_payload(payload)
        assert "underlying ValueError" in str(excinfo.value)
        assert isinstance(excinfo.value.__cause__, ValueError)


if __name__ == "__main__":
    pytest.main([__file__])
