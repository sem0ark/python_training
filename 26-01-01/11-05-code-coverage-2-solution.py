import functools

import pytest

# ===============================================================
# SYSTEM UNDER TEST (The code to cover)
# ===============================================================


def audit(func):
    """
    An 'Overzealous Supervisor' decorator for tracking execution metrics.
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

    def test_audit_successful_call(self):
        """Verify metrics on a successful call."""

        @audit
        def add(a, b):
            return a + b

        assert add.audit_data["call_count"] == 0
        assert add(2, 3) == 5
        assert add.audit_data["call_count"] == 1
        assert add.audit_data["last_exception"] is None

    def test_audit_failed_call_propagation(self):
        """Verify metrics on a failed call and that exception propagates."""

        @audit
        def crack():
            raise ValueError("Cracked!")

        assert crack.audit_data["call_count"] == 0
        with pytest.raises(ValueError) as excinfo:
            crack()

        assert str(excinfo.value) == "Cracked!"
        assert crack.audit_data["call_count"] == 1
        assert isinstance(crack.audit_data["last_exception"], ValueError)

    def test_audit_reset_success_after_failure(self):
        """Verify last_exception is reset to None after a successful call."""

        @audit
        def toggle(fail=False):
            if fail:
                raise RuntimeError("Fail")
            return "OK"

        with pytest.raises(RuntimeError):
            toggle(fail=True)
        assert toggle.audit_data["last_exception"] is not None

        assert toggle(fail=False) == "OK"
        assert toggle.audit_data["call_count"] == 2
        assert toggle.audit_data["last_exception"] is None

    def test_audit_method_support(self):
        """Verify decorator works on class methods."""

        class Bank:
            @audit
            def withdraw(self, amount):
                return f"Withdrew {amount}"

        b = Bank()
        assert b.withdraw(100) == "Withdrew 100"
        assert b.withdraw.audit_data["call_count"] == 1


if __name__ == "__main__":
    pytest.main([__file__])
