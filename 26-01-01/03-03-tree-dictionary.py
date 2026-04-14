from collections import defaultdict

import pytest

"""
Goal: Build a "tree" structure where you can assign values 
to deeply nested keys without initializing every level.

Example:
tree['users']['admin']['permissions'] = 'all'

Requirements:
1. Implement a function `get_tree()` that returns a defaultdict.
2. The defaultdict should automatically return another 
   defaultdict when a missing key is accessed.
"""


def get_tree():
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_recursive_tree():
    tree = get_tree()
    tree["a"]["b"]["c"] = 100

    assert "a" in tree
    assert "b" in tree["a"]
    assert tree["a"]["b"]["c"] == 100


def test_default_type():
    tree = get_tree()
    assert isinstance(tree["new_key"], defaultdict)


if __name__ == "__main__":
    pytest.main([__file__])
