import pytest

"""
Goal: Re-implement `functools.partial` from scratch.

Description:
Partial application allows you to "freeze" a portion of a function's 
arguments and/or keywords, resulting in a new object with a simplified 
signature.

Requirements:
1. Create a function `my_partial(func, *fixed_args, **fixed_kwargs)`.
2. It must return a callable (a function or an object).
3. When the returned callable is invoked with `*args` and `**kwargs`:
   - The `fixed_args` must come BEFORE the new `args`.
   - The `fixed_kwargs` and new `kwargs` must be merged.
   - If a keyword is present in both, the NEWEST value (from the call) 
     should overwrite the fixed one.
4. The original function `func` should then be called with these merged arguments.

Concepts: Variadic arguments (*args, **kwargs), Closures, Argument Merging.
"""


def my_partial(func, *fixed_args, **fixed_kwargs):
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_partial_positional():
    """Tests basic positional argument freezing."""

    def add(a, b):
        return a + b

    add_five = my_partial(add, 5)
    assert add_five(10) == 15
    assert add_five(20) == 25


def test_partial_multiple_args():
    """Tests freezing multiple positional arguments."""

    def multiply_four(a, b, c, d):
        return a * b * c * d

    # Freeze first two: 2 * 3 = 6. Then 6 * (call_args)
    double_triple = my_partial(multiply_four, 2, 3)
    assert double_triple(4, 5) == 120  # 2 * 3 * 4 * 5


def test_partial_keywords():
    """Tests freezing keyword arguments."""

    def power(base, exponent):
        return base**exponent

    square = my_partial(power, exponent=2)
    cube = my_partial(power, exponent=3)

    assert square(5) == 25
    assert cube(5) == 125


def test_partial_keyword_overwrite():
    """Tests that call-time keywords override fixed keywords."""

    def greet(name, greeting="Hello"):
        return f"{greeting}, {name}!"

    # Fixed greeting is "Hi"
    hi_greet = my_partial(greet, greeting="Hi")

    assert hi_greet("Bob") == "Hi, Bob!"
    # Call-time overwrite: "Hi" becomes "Goodbye"
    assert hi_greet("Bob", greeting="Goodbye") == "Goodbye, Bob!"


def test_partial_mixed_complex():
    """Tests a complex mix of positional and keyword arguments."""

    def complex_func(*args, **kwargs):
        return args, kwargs

    p = my_partial(complex_func, 1, 2, a="apple", b="banana")

    final_args, final_kwargs = p(3, b="blueberry", c="cherry")

    assert final_args == (1, 2, 3)
    assert final_kwargs == {"a": "apple", "b": "blueberry", "c": "cherry"}


if __name__ == "__main__":
    pytest.main([__file__])
