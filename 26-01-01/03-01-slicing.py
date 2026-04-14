import pytest

"""
Goal: Extract specific patterns from sequences using slices.

Requirements:
1. Implement `get_753(string)`: From '123456789', return '753'.
2. Implement `reverse_words(sentence)`: Reverse the order of words 
   in a string using slicing/joining.
3. Implement `get_every_third_reversed(data)`: Return every 3rd 
   element starting from the end.

Concepts: Negative steps, start/stop boundaries.
"""


def get_753(s):
    # TODO: Return '753' from '123456789'
    raise NotImplementedError()


def reverse_words(sentence):
    # TODO: "Hello World" -> "World Hello"
    raise NotImplementedError()


def get_every_third_reversed(lst):
    # TODO: [0, 1, 2, 3, 4, 5, 6] -> [6, 3, 0]
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_slicing_753():
    assert get_753("123456789") == "753"


def test_reverse_words():
    assert reverse_words("Python is great") == "great is Python"


def test_every_third():
    assert get_every_third_reversed(list(range(10))) == [9, 6, 3, 0]


if __name__ == "__main__":
    pytest.main([__file__])
