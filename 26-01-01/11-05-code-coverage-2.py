import functools

import pytest

# ===============================================================
# SYSTEM UNDER TEST (The code to cover)
# ===============================================================


def audit(func):
    """
    An 'Overzealous Supervisor' decorator for tracking execution metrics.

    Requirements:
    1. Preserve the original function's __name__, __doc__, and signature.
    2. Attach an 'audit_data' dictionary to the decorated function.
    3. Increment 'call_count' on every invocation (success or failure).
    4. Store the most recent exception instance in 'last_exception'.
    5. Set 'last_exception' to None if the most recent call was successful.
    6. Ensure all exceptions propagate to the caller.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            wrapper.audit_data["last_exception"] = None
            return result
        except Exception as e:
            wrapper.audit_data["last_exception"] = e
            raise
        finally:
            wrapper.audit_data["call_count"] += 1

    wrapper.audit_data = {"call_count": 0, "last_exception": None}
    return wrapper


# ===============================================================
# TESTS
# ===============================================================


class TestAuditor:
    """
    Goal: Reach 100% branch coverage for the audit decorator.
    """

    def test_audit_metadata_preservation(self):
        """Verify that the decorator preserves function metadata."""

        @audit
        def trade_stocks(symbol: str):
            """Executes a high-frequency trade."""
            return f"Traded {symbol}"

        assert trade_stocks.__name__ == "trade_stocks"
        assert trade_stocks.__doc__ == "Executes a high-frequency trade."
        assert "symbol" in trade_stocks.__annotations__

    # TODO: Add more tests below to cover all branches:
    # - Successful call: verify call_count increments and last_exception is None.
    # - Failed call: verify call_count increments and last_exception stores the error.
    # - Exception propagation: verify the decorator does not swallow errors.
    # - Method support: verify it works on methods inside a class.
    # - Sequence: verify success after failure resets last_exception to None.


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - To test exception branches, use `with pytest.raises(YourException):`.
# - For method testing, define a class inside the test function and apply @audit to one of its methods.
# - Branch coverage requires hitting both the 'try' success path and the 'except' failure path.
# - The 'finally' block is executed in both cases, but ensuring it runs after an exception is part of the contract.
