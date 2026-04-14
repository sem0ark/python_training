"""
"Auditable" Number Class

Implement a class called `Number` that acts like a numeric type (int/float)
but tracks the history of every mathematical operation performed on it.

Requirements:
1. Initialization:
   - A new `Number` instance should accept a value.
   - If it's a "leaf" number (e.g., Number(5)), its history is just "5".

2. Arithmetic Operations:
   - Implement `+, -, *, /`.
   - Each operation must return a NEW `Number` instance.
   - The new instance's value should be the result of the math.
   - The new instance's history should be a string: "(left_history op right_history)".

3. String Representation:
   - `__str__` must return the history string.
   - `__repr__` should return a string like: Number(value=10, history='(5 + 5)')

4. Type Coercion:
   - The class should support operations with regular Python numbers (int/float).
   - Example: `Number(5) + 10` should result in a history of "(5 + 10)".

5. Error Handling:
   - Standard math errors (like ZeroDivisionError) should still be raised.

Example:
    n1 = Number(1)
    n2 = Number(2)
    res = (n1 + n2) * 3
    print(res)        # Output: "((1 + 2) * 3)"
    print(res.value)  # Output: 9
"""

import pytest


class Number:
    """Implements a number that tracks its history of operations."""

    def __init__(self, value, history=None):
        self.value = value
        self.history = history if history is not None else str(value)

    def __str__(self):
        return self.history

    def __repr__(self):
        return f"Number(value={self.value}, history='{self.history}')"

    def _operate(self, other, operator):
        if isinstance(other, (int, float)):
            other_value = other
            other_history = str(other)
        elif isinstance(other, Number):
            other_value = other.value
            other_history = other.history
        else:
            return NotImplemented

        if operator == "+":
            new_value = self.value + other_value
        elif operator == "-":
            new_value = self.value - other_value
        elif operator == "*":
            new_value = self.value * other_value
        elif operator == "/":
            if other_value == 0:
                raise ZeroDivisionError("division by zero")
            new_value = self.value / other_value
        else:
            raise ValueError("Unsupported operator")

        new_history = f"({self.history} {operator} {other_history})"
        return Number(new_value, new_history)

    def __add__(self, other):
        return self._operate(other, "+")

    def __sub__(self, other):
        return self._operate(other, "-")

    def __mul__(self, other):
        return self._operate(other, "*")

    def __truediv__(self, other):
        return self._operate(other, "/")


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_initial_state():
    n = Number(10)
    assert n.value == 10
    assert str(n) == "10"


def test_simple_addition():
    res = Number(1) + Number(2)
    assert res.value == 3
    assert str(res) == "(1 + 2)"


def test_chained_operations():
    # ((1 + 2) * 3)
    res = (Number(1) + Number(2)) * Number(3)
    assert res.value == 9
    assert str(res) == "((1 + 2) * 3)"


def test_mixed_types():
    # Supports regular integers
    res = Number(10) - 5
    assert res.value == 5
    assert str(res) == "(10 - 5)"


def test_complex_history():
    # ((10 / 2) + (1 * 4))
    n1 = Number(10) / 2
    n2 = Number(1) * 4
    res = n1 + n2
    assert res.value == 9.0
    assert str(res) == "((10 / 2) + (1 * 4))"


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        _ = Number(10) / 0


def test_repr_format():
    n = Number(5) + 5
    expected = "Number(value=10, history='(5 + 5)')"
    assert repr(n) == expected


if __name__ == "__main__":
    pytest.main([__file__])
