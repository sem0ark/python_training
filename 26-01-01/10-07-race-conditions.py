import threading

import pytest

"""
Demonstrate that concurrent increments require synchronization to preserve correctness.

Requirements:
1. `UnsafeCounter.increment()` must be a non-thread-safe increment operation that may lose updates under contention.
2. `SafeCounter.increment()` must guarantee correctness under concurrent use.
3. Both classes must implement the integer protocol so `int(instance)` returns the current value.
4. `CounterBench.stress_test(counter_instance, threads, iterations)` must run concurrent increments and wait for completion.
5. Tests will assert that `UnsafeCounter` typically loses updates under high contention while `SafeCounter` reaches the expected total.
"""


class UnsafeCounter:
    def __init__(self):
        self.value = 0

    def increment(self):
        raise NotImplementedError()

    def __int__(self):
        raise NotImplementedError()


class SafeCounter:
    def __init__(self):
        self.value = 0
        raise NotImplementedError()

    def increment(self):
        raise NotImplementedError()

    def __int__(self):
        raise NotImplementedError()


class CounterBench:
    @staticmethod
    def stress_test(counter, thread_count: int, iterations: int):
        """Spawns threads to increment the counter concurrently."""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_unsafe_counter_race_condition():
    """Verify that unsafe increments lead to data loss."""
    counter = UnsafeCounter()
    threads = 10
    iters = 50000  # High enough to trigger context switches during +=

    CounterBench.stress_test(counter, threads, iters)

    # Expected: 500,000. Actual: likely much less.
    # The GIL is released every 5ms (sys.setswitchinterval),
    # ensuring threads interrupt each other during the Read-Modify-Write cycle.
    assert int(counter) < (threads * iters)


def test_safe_counter_integrity():
    """Verify that explicit locking prevents data loss."""
    counter = SafeCounter()
    threads = 10
    iters = 50000

    CounterBench.stress_test(counter, threads, iters)

    assert int(counter) == (threads * iters)


def test_counter_protocols():
    """Verify dunder method implementation."""
    c = SafeCounter()
    c.increment()
    assert int(c) == 1
    assert isinstance(int(c), int)


def test_lock_isolation():
    """Ensure each SafeCounter instance has its own independent lock."""
    c1 = SafeCounter()
    c2 = SafeCounter()
    # If they shared a lock, performance would tank, but here we check state
    c1.increment()
    assert int(c1) == 1
    assert int(c2) == 0


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - The operation `self.value += 1` is actually three bytecode instructions:
#   LOAD_ATTR, BINARY_ADD, STORE_ATTR. The GIL can be released between these.
# - Use `threading.Lock` as a context manager inside `SafeCounter.increment`.
# - Ensure `stress_test` waits for all threads to finish (`join`) before returning.
