import pytest

# ===============================================================
# SYSTEM UNDER TEST (The code to cover)
# ===============================================================


class SecurityEvent:
    """
    A 'Digital Notary' record that enforces immutability and memory efficiency.
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

    def test_immutability_setattr(self):
        """Verify __setattr__ raises AttributeError."""
        event = SecurityEvent(1, "2023-10-01", "LOGIN")
        with pytest.raises(AttributeError) as excinfo:
            event.action = "LOGOUT"
        assert "immutable" in str(excinfo.value)

    def test_immutability_delattr(self):
        """Verify __delattr__ raises AttributeError."""
        event = SecurityEvent(1, "2023-10-01", "LOGIN")
        with pytest.raises(AttributeError) as excinfo:
            del event.action
        assert "immutable" in str(excinfo.value)

    def test_equality_and_inequality(self):
        """Verify __eq__ logic for identical and different objects."""
        e1 = SecurityEvent(1, "2023-10-01", "LOGIN")
        e2 = SecurityEvent(1, "2023-10-01", "LOGIN")
        e3 = SecurityEvent(2, "2023-10-01", "LOGIN")

        assert e1 == e2
        assert e1 != e3

    def test_equality_not_implemented(self):
        """Verify __eq__ returns NotImplemented for non-SecurityEvent types."""
        event = SecurityEvent(1, "2023-10-01", "LOGIN")
        # Comparing with a string should return False as __eq__ returns NotImplemented
        assert event != "some string"

    def test_hashability(self):
        """Verify the object is hashable and can be used in a set."""
        event = SecurityEvent(1, "2023-10-01", "LOGIN")
        s = {event}
        assert event in s
        assert hash(event) == hash((1, "2023-10-01", "LOGIN"))

    def test_memory_optimization(self):
        """Verify that the instance does not have a __dict__ attribute."""
        event = SecurityEvent(1, "2023-10-01", "LOGIN")
        assert not hasattr(event, "__dict__")
        assert "__slots__" in SecurityEvent.__dict__


if __name__ == "__main__":
    pytest.main([__file__])
