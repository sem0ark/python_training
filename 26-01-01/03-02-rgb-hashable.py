import pytest

"""
Goal: Create a `Color` class that can be used as a key in a dictionary.

Requirements:
1. The class should take `r`, `g`, `b` (integers).
2. It must be immutable (hint: use a tuple internally or don't allow changes).
3. Implement `__eq__`: Colors are equal if their RGB values are identical.
4. Implement `__hash__`: Generate a hash based on the RGB values.

Concepts: Hashability, Equality, dict keys.
"""


class Color:
    def __init__(self, r, g, b):
        self._r = r
        self._g = g
        self._b = b

    # TODO: Implement __eq__ and __hash__
    pass


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_color_as_dict_key():
    c1 = Color(255, 0, 0)
    c2 = Color(255, 0, 0)
    palette = {c1: "Red"}

    # Even if objects are different instances, equality/hash should allow lookup
    assert palette[c2] == "Red"
    assert len(palette) == 1


def test_color_set_uniqueness():
    colors = {Color(0, 0, 0), Color(0, 0, 0), Color(1, 1, 1)}
    assert len(colors) == 2


if __name__ == "__main__":
    pytest.main([__file__])
