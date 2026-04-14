import pytest

"""
Goal: Implement a function `multiply` that can be called 
repeatedly to accumulate values.

Requirements:
1. It should accept any number of positional arguments: multiply(1, 2, 3)
2. It should be chainable: multiply(1)(2, 3)(4)
3. When called with NO arguments, it should return the final product of all numbers: multiply(1)(2)() -> 3
4. Special Case: If the very first call is empty, return None: multiply() -> None

Hints:
- You will need a nested function (closure).
- The outer function handles the initial call.
- The inner function updates a total and returns itself to allow chaining.
- We can avoid using `nonlocal` to avoid mutable state entirely.
"""


def multiply(*args):
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_multiply_basic():
    assert multiply(1, 2, 3)() == 6


def test_multiply_chained():
    assert multiply(1)(2)(3)() == 6


def test_multiply_mixed():
    assert multiply(1, 2)(3, 4)() == 24


def test_multiply_none():
    assert multiply() is None


def test_multiply_deep_chain():
    assert multiply(10)(-5)(2, 3)() == -300
    assert multiply(10)(-5)(2, 3)(0)() == 0
    assert multiply(0)(10)(-5)(2, 3)() == 0


def test_multiply_immutability():
    six = multiply(2, 3)
    assert six(3)() == 18
    assert six(2)() == 12
    assert six(0)() == 0


if __name__ == "__main__":
    pytest.main([__file__])
