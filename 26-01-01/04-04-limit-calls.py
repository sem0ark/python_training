from functools import wraps

import pytest

"""
Goal: Implement a parameterized decorator `@limit_calls(n)` 
that restricts how many times a function can be executed.

Requirements:
1. It should accept an integer `n` as an argument.
2. It should allow the decorated function to run `n` times.
3. On the `n+1` call, it should raise a `ValueError`.
4. It must use `functools.wraps` to preserve the original 
   function's name and docstring.
5. The call count must be stored in a closure (not a global variable).

Concepts: Decorators, Parameterized Decorators, Closures, functools.wraps.
"""


def limit_calls(n):
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_limit_behavior():
    """Tests that the function stops working after n calls."""

    @limit_calls(2)
    def test_func():
        return "Success"

    assert test_func() == "Success"  # Call 1
    assert test_func() == "Success"  # Call 2
    with pytest.raises(ValueError):
        test_func()  # Call 3 - Should fail


def test_metadata_preservation():
    """Tests if the decorator preserves __name__ and __doc__."""

    @limit_calls(5)
    def named_func():
        """This is a docstring."""
        pass

    assert named_func.__name__ == "named_func"
    assert named_func.__doc__ == "This is a docstring."


def test_independent_counters():
    """Tests that two decorated functions have separate counters."""

    @limit_calls(1)
    def func_a():
        return "a"

    @limit_calls(1)
    def func_b():
        return "b"

    assert func_a() == "a"
    assert func_b() == "b"
    with pytest.raises(ValueError):
        func_a()


if __name__ == "__main__":
    pytest.main([__file__])
