from copy import deepcopy

import pytest

"""
Goal: Debug a multi-layered state leak involving nested objects and aliasing.

You are building a system for a Kiosk Franchise. Each `Kiosk` has a 
`KioskConfig` object that holds the inventory and a list of audit logs.

Though, the code behaves quite strange from time to time, could you fix it?

Concepts: Nested Mutable Defaults, Object Aliasing, Deep vs Shallow Copy.
"""


class KioskConfig:
    def __init__(self, inventory={}, logs=[]):
        self.inventory = inventory
        self.logs = logs


class Kiosk:
    def __init__(self, config=KioskConfig()):
        self.config = config

    def add_article(self, name, count):
        self.config.inventory[name] = self.config.inventory.get(name, 0) + count
        self.config.logs.append(f"Added {count} {name}")


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_default_kiosks_independence():
    """Default kiosks should not share inventory or logs."""
    k1 = Kiosk()
    k2 = Kiosk()

    k1.add_article("apple", 5)

    assert "apple" in k1.config.inventory
    assert len(k1.config.logs) == 1

    # If the bug exists, k2 will have k1's apples and logs
    assert "apple" not in k2.config.inventory, (
        "Kiosk 2 inherited inventory from Kiosk 1!"
    )
    assert len(k2.config.logs) == 0, "Kiosk 2 inherited logs from Kiosk 1!"


def test_external_data_protection():
    """Modifying a Kiosk should not modify the dictionary passed into it."""
    user_inventory = {"bread": 1}
    user_logs = ["Initial stock"]

    custom_config = KioskConfig(inventory=user_inventory, logs=user_logs)
    k3 = Kiosk(config=custom_config)

    k3.add_article("bread", 10)

    # The Kiosk should have 11 bread
    assert k3.config.inventory["bread"] == 11
    # The original user_inventory should remain UNCHANGED (Encapsulation)
    assert user_inventory["bread"] == 1, "The Kiosk corrupted the caller's dictionary!"
    assert len(user_logs) == 1, "The Kiosk corrupted the caller's log list!"


def test_deep_config_isolation():
    """Ensure that even nested objects are independent."""
    k1 = Kiosk()
    k2 = Kiosk()
    assert k1.config is not k2.config
    assert k1.config.inventory is not k2.config.inventory
    assert k1.config.logs is not k2.config.logs


if __name__ == "__main__":
    pytest.main([__file__])
