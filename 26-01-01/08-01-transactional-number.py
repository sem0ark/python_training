"""
Build a transactional calculation system where numbers track their 
history, and operations can be rolled back if an error occurs.

Requirements:
1. Define a custom exception `AuditError`.
2. Number Class:
    - Implement initialization to store a numeric `value` and a string `history`.
    - If no history is provided during initialization, use the string 
      representation of the value.
    - Implement common operations + - *
        - Support operations with other `Number` instances or raw numeric types.
        - Return a new `Number` instance.
        - Update the history to reflect the operation in the format: `(left + right)`.
    - Implement division /
        - Support operations with other `Number` instances or raw numeric types.
        - Update the history to reflect the operation in the format: (left / right).
        - If the operation results in a division by zero, raise an `AuditError` 
          with the message "Calculation failed".
        - Ensure the original error is attached to the `AuditError`.
3. Transactional Context Manager:
    - Implement a class named `Transactional` that follows the context manager protocol.
    - It should be initialized with a `Number` instance.
    - Upon entering the block, it should capture the current state of the number.
    - Upon exiting the block:
        - If the block finished successfully, the changes to the number are kept.
        - If any exception occurred, the number must be restored to its exact 
          state from before the block started.
        - The context manager must not silence any exceptions.

Example:
    n = Number(10)
    try:
        with Transactional(n):
            n = n / 0
    except AuditError:
        print(n.value) # Output: 10 (reverted due to error)
"""

import pytest


class AuditError(Exception):
    pass


class Number:
    pass


class Transactional:
    pass


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_number_init():
    """Basic initialization of value and history."""
    n = Number(10)
    assert n.value == 10
    assert n.history == "10"


def test_number_history_addition():
    """History string builds correctly during addition."""
    n = Number(5) + 5
    assert n.value == 10
    assert n.history == "(5 + 5)"


def test_number_history_chaining():
    """History string nests correctly across multiple operations."""
    n = (Number(1) + 2) + 3
    assert n.value == 6
    assert n.history == "((1 + 2) + 3)"


def test_audit_error_raised():
    """Custom AuditError is raised on zero division."""
    n = Number(10)
    with pytest.raises(AuditError):
        _ = n / 0


def test_exception_chaining_integrity():
    """AuditError preserves ZeroDivisionError as its cause."""
    n = Number(10)
    try:
        _ = n / 0
    except AuditError as e:
        assert isinstance(e.__cause__, ZeroDivisionError)
        assert "Calculation failed" in str(e)


def test_transaction_commit():
    """Changes inside a successful transaction are kept."""
    n = Number(10)
    with Transactional(n):
        res = n + 5
        n.value, n.history = res.value, res.history

    assert n.value == 15
    assert n.history == "(10 + 5)"


def test_transaction_rollback_on_audit_error():
    """State reverts to original if an AuditError occurs."""
    n = Number(10)
    try:
        with Transactional(n):
            res = n + 50
            n.value, n.history = res.value, res.history
            _ = n / 0  # Raises AuditError
    except AuditError:
        pass

    assert n.value == 10
    assert n.history == "10"


def test_transaction_rollback_on_generic_error():
    """State reverts on any exception (e.g., ValueError)."""
    n = Number(10)
    try:
        with Transactional(n):
            n.value = 999
            raise ValueError("Random crash")
    except ValueError:
        pass

    assert n.value == 10


def test_transaction_exception_propagation():
    """Transactional does not swallow exceptions."""
    n = Number(1)
    with pytest.raises(RuntimeError):
        with Transactional(n):
            raise RuntimeError("Should propagate")


def test_transaction_isolation():
    """Modifying attributes doesn't affect the snapshot."""
    n = Number(100)
    try:
        with Transactional(n):
            n.value = 200
            # Even if we delete attributes, they should be restored
            del n.history
            raise Exception()
    except Exception:
        pass
    assert n.value == 100
    assert n.history == "100"


if __name__ == "__main__":
    pytest.main([__file__])
