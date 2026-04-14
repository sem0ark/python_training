import pytest

"""
Goal: Fix the "Late Binding" bug in a list of lambda functions.

Description:
The function `create_incrementors` is intended to return a list of 
functions where the first adds 0, the second adds 1, and so on. 
However, due to Python's late binding in closures, they all 
currently add the same (final) value of 'i'.

Task:
Modify the lambda definition inside the loop so that the 
current value of 'i' is "captured" at the moment the lambda 
is created.

Hint: Use a default argument (e.g., `arg=arg`) inside the lambda.
"""


def create_incrementors(n):
    funcs = []
    for i in range(n):
        # TODO: Fix the lambda below
        funcs.append(lambda x: x + i)
    return funcs


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_incrementors_logic():
    """Tests if each function captures its own index 'i'."""
    incrementors = create_incrementors(3)
    assert incrementors[0](10) == 10
    assert incrementors[1](10) == 11
    assert incrementors[2](10) == 12


def test_list_length():
    """Tests that the correct number of functions are created."""
    assert len(create_incrementors(5)) == 5


if __name__ == "__main__":
    pytest.main([__file__])
