import multiprocessing
import time

import pytest

"""
Demonstrate and resolve race conditions in shared memory across processes.

Requirements:
1. `GossipCounter` must expose a process-shared integer value accessible to multiple processes.
2. `increment_unprotected` must increment the shared value without synchronization and may lose updates under contention.
3. `increment_protected` must increment the shared value safely under concurrent processes.
4. Tests will show that unprotected increments suffer data loss while protected increments remain correct.
"""


class GossipCounter:
    def __init__(self, initial_value: int = 0):
        raise NotImplementedError()

    def increment_unprotected(self):
        """Increments the shared value without using a lock."""
        raise NotImplementedError()

    def increment_protected(self):
        """Increments the shared value using a multiprocessing.Lock."""
        raise NotImplementedError()

    @property
    def value(self):
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def run_parallel_increments(method_name, iterations, process_count):
    counter = GossipCounter(0)

    def worker(cnt, iters, attr):
        func = getattr(cnt, attr)
        for _ in range(iters):
            func()

    processes = [
        multiprocessing.Process(target=worker, args=(counter, iterations, method_name))
        for _ in range(process_count)
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    return counter.value


def test_protected_increments_are_accurate():
    # 4 processes * 1000 increments should be exactly 4000
    total = run_parallel_increments("increment_protected", 1000, 4)
    assert total == 4000


def test_unprotected_increments_suffer_race_conditions():
    # Under high load, unprotected increments will almost certainly fail to reach the total
    # because 'val += 1' is not atomic (Read, Increment, Write)
    total = run_parallel_increments("increment_unprotected", 2000, 4)
    # It is statistically improbable to hit 8000 without a lock
    assert total < 8000


def test_value_isolation():
    c1 = GossipCounter(10)
    c2 = GossipCounter(20)
    assert c1.value == 10
    assert c2.value == 20


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - `multiprocessing.Value` objects have a built-in `.get_lock()` method,
#   but you can also pass an explicit Lock object.
# - Even though `Value` has a lock, the Python operation `shared.value += 1`
#   is NOT atomic because it involves a read and a write step.
