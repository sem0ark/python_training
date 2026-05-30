import pytest

# ===============================================================
# SYSTEM UNDER TEST (The code to cover)
# ===============================================================


class SecurityEvent:
    """
    A 'Digital Notary' record that enforces immutability and memory efficiency.

    Requirements:
    1. Accept event_id, timestamp, and action during instantiation.
    2. Raise AttributeError on any attempt to modify or delete attributes.
    3. Equality is based on identical attribute values.
    4. Instances must be hashable (usable in sets and as dict keys).
    5. Optimize memory by preventing the creation of __dict__.
    6. __repr__ format: SecurityEvent(event_id=..., timestamp=..., action=...)
    """

    __slots__ = ("event_id", "timestamp", "action")

    def __init__(self, event_id, timestamp, action):
        # Using object.__setattr__ to bypass the immutability logic during init
        object.__setattr__(self, "event_id", event_id)
        object.__setattr__(self, "timestamp", timestamp)
        object.__setattr__(self, "action", action)

    def __setattr__(self, name, value):
        raise AttributeError(f"SecurityEvent is immutable; cannot modify '{name}'")

    def __delattr__(self, name):
        raise AttributeError(f"SecurityEvent is immutable; cannot delete '{name}'")

    def __eq__(self, other):
        if not isinstance(other, SecurityEvent):
            return NotImplemented
        return (
            self.event_id == other.event_id
            and self.timestamp == other.timestamp
            and self.action == other.action
        )

    def __hash__(self):
        return hash((self.event_id, self.timestamp, self.action))

    def __repr__(self):
        return (
            f"SecurityEvent(event_id={self.event_id!r}, "
            f"timestamp={self.timestamp!r}, action={self.action!r})"
        )


# ===============================================================
# TESTS
# ===============================================================


class TestSecurityEvent:
    """
    Goal: Reach 100% branch coverage for the SecurityEvent class.
    """

    def test_initialization_and_repr(self):
        """Verify attributes are set correctly and repr matches specification."""
        event = SecurityEvent(1, "2023-10-01", "LOGIN")
        assert event.event_id == 1
        assert event.timestamp == "2023-10-01"
        assert event.action == "LOGIN"
        assert (
            repr(event)
            == "SecurityEvent(event_id=1, timestamp='2023-10-01', action='LOGIN')"
        )

    # TODO: Add more tests below to reach 100% coverage:
    # - Immutability: Verify __setattr__ raises AttributeError.
    # - Immutability: Verify __delattr__ raises AttributeError.
    # - Equality: Compare two identical objects.
    # - Equality: Compare two different objects.
    # - Equality: Compare with a non-SecurityEvent object (e.g., a string or int).
    # - Hashability: Verify the object can be added to a set.
    # - Memory: Verify that the instance does not have a __dict__ attribute.


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - To verify memory optimization, check `hasattr(obj, '__dict__')`.
# - For the `NotImplemented` branch in `__eq__`, compare a `SecurityEvent` instance to a different type.
# - Use `pytest.raises(AttributeError)` to test the protection against modification and deletion.
# - Remember that `__slots__` is a class-level attribute; it prevents the creation of `__dict__` on instances.
