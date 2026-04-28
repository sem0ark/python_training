import threading

import pytest

"""
Implement a TransactionManager that safely acquires multiple locks to prevent deadlocks.

Requirements:
1. The 'execute_transfer' method must acquire locks for all involved accounts before proceeding.
2. It must be impossible for two concurrent transfers between the same two accounts to deadlock.
3. The system must support an arbitrary number of accounts.
4. Locks must be released regardless of whether the transfer succeeds or raises an exception.
"""


class Account:
    def __init__(self, account_id: int):
        self.account_id = account_id
        self.lock = threading.Lock()
        self.balance = 100


class TransactionManager:
    def execute_transfer(self, source: Account, destination: Account, amount: int):
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_transfer_success():
    tm = TransactionManager()
    acc1, acc2 = Account(1), Account(2)
    tm.execute_transfer(acc1, acc2, 50)
    assert acc1.balance == 50
    assert acc2.balance == 150


def test_transfer_atomic_locking():
    # This test checks if locks are released
    tm = TransactionManager()
    acc1, acc2 = Account(1), Account(2)
    tm.execute_transfer(acc1, acc2, 10)

    # If locks weren't released, this would hang
    assert acc1.lock.acquire(blocking=False)
    acc1.lock.release()


def test_deadlock_prevention():
    tm = TransactionManager()
    acc1 = Account(1)
    acc2 = Account(2)

    def transfer_1_to_2():
        for _ in range(1000):
            tm.execute_transfer(acc1, acc2, 1)

    def transfer_2_to_1():
        for _ in range(1000):
            tm.execute_transfer(acc2, acc1, 1)

    t1 = threading.Thread(target=transfer_1_to_2)
    t2 = threading.Thread(target=transfer_2_to_1)

    t1.start()
    t2.start()
    t1.join(timeout=5)
    t2.join(timeout=5)

    assert not t1.is_alive(), "Potential deadlock detected: Thread 1 hung"
    assert not t2.is_alive(), "Potential deadlock detected: Thread 2 hung"


def test_transfer_exception_safety():
    tm = TransactionManager()
    acc1, acc2 = Account(1), Account(2)

    with pytest.raises(ValueError):
        tm.execute_transfer(acc1, acc2, 1000)  # Assuming insufficient funds logic

    assert acc1.lock.acquire(blocking=False), "Lock not released after exception"
    acc1.lock.release()


def test_transaction_manager_isolation():
    # Two managers operating on different account pairs should not interfere
    tm1 = TransactionManager()
    tm2 = TransactionManager()
    a1, a2 = Account(1), Account(2)
    b1, b2 = Account(3), Account(4)

    def t1():
        tm1.execute_transfer(a1, a2, 10)

    def t2():
        tm2.execute_transfer(b1, b2, 20)

    th1 = threading.Thread(target=t1)
    th2 = threading.Thread(target=t2)
    th1.start()
    th2.start()
    th1.join()
    th2.join()

    assert a1.balance == 90 and a2.balance == 110
    assert b1.balance == 80 and b2.balance == 120


def test_transfer_invalid_amount_raises():
    tm = TransactionManager()
    acc1, acc2 = Account(1), Account(2)
    with pytest.raises(ValueError):
        tm.execute_transfer(acc1, acc2, -10)

    # Ensure locks are released after invalid input
    assert acc1.lock.acquire(blocking=False)
    acc1.lock.release()


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - To prevent circular wait, establish a global order for lock acquisition.
# - Compare account IDs to decide which lock to acquire first, regardless of which is 'source' or 'destination'.
