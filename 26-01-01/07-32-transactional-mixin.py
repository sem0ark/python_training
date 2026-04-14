import pytest


class Transactional:
    """
    Mixin that allows an object to roll back its attributes
    if exception occurs within a 'with' block.
    """


class Account(Transactional):
    def __init__(self, balance):
        self.balance = balance


def test_rollback_on_failure():
    acc = Account(100)
    try:
        with acc:
            acc.balance = 500
            raise ValueError("Bank error")
    except ValueError:
        pass

    assert acc.balance == 100
    assert "_snapshot" not in acc.__dict__


def test_commit_on_success():
    acc = Account(100)
    with acc:
        acc.balance = 200

    assert acc.balance == 200
    assert "_snapshot" not in acc.__dict__


def test_nested_attribute_addition():
    acc = Account(100)
    try:
        with acc:
            acc.new_attr = "temporary"
            raise Exception()
    except:
        pass

    assert not hasattr(acc, "new_attr")
    assert "_snapshot" not in acc.__dict__


def test_multiple_successive_transactions():
    acc = Account(100)
    with acc:
        acc.balance = 200
    with acc:
        acc.balance = 300
    assert acc.balance == 300
    assert "_snapshot" not in acc.__dict__


def test_snapshot_cleanup():
    acc = Account(100)
    with acc:
        pass
    assert "_snapshot" not in acc.__dict__


if __name__ == "__main__":
    pytest.main([__file__])
