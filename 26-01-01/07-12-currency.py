"""
Financial Currency Arithmetic

Use operator overloading to allow adding different amounts of money, ensuring we don't accidentally add two different currencies together.
"""

import pytest


class Price:
    """
    Requirements:
    1. `__add__`: Allow `Price + Price`. If currencies differ, raise ValueError.
    2. `__repr__`: Return string like "Price(100, 'USD')".
    3. `__eq__`: Prices are equal if amount and currency match.
    """

    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __add__(self, other):
        raise NotImplementedError()

    def __repr__(self):
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_price_addition():
    p1 = Price(10, "USD")
    p2 = Price(20, "USD")
    p3 = p1 + p2
    assert p3.amount == 30
    assert p3.currency == "USD"


def test_price_mismatch():
    p1 = Price(10, "USD")
    p2 = Price(10, "EUR")
    with pytest.raises(ValueError):
        _ = p1 + p2


def test_price_repr():
    assert repr(Price(50, "GBP")) == "Price(50, 'GBP')"


def test_price_equality():
    assert Price(10, "USD") == Price(10, "USD")
    assert Price(10, "USD") != Price(20, "USD")


def test_price_equality_different_type():
    assert Price(10, "USD") != "10 USD"


def test_price_zero_addition():
    p = Price(0, "JPY") + Price(100, "JPY")
    assert p.amount == 100


if __name__ == "__main__":
    pytest.main([__file__])
