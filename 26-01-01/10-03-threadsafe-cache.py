import time
from functools import wraps

import pytest

"""
Implement a 'latency_cache' decorator for signal processing functions.

Requirements:
1. It must cache the return value of a function based on its input arguments.
2. Cached values must expire after 'ttl_seconds'.
3. The decorator must preserve the original function's __name__, __doc__, and __annotations__.
4. It must be thread-safe, ensuring that two threads don't compute the same expired signal simultaneously.
"""


def latency_cache(ttl_seconds: float):
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_cache_expiration():
    call_count = 0

    @latency_cache(ttl_seconds=0.1)
    def get_signal(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert get_signal(5) == 10
    assert get_signal(5) == 10
    assert call_count == 1

    time.sleep(0.15)
    assert get_signal(5) == 10
    assert call_count == 2


def test_metadata_preservation():
    @latency_cache(ttl_seconds=1.0)
    def process_data(a: int) -> int:
        """Process the data."""
        return a

    assert process_data.__name__ == "process_data"
    assert process_data.__doc__ == "Process the data."
    assert process_data.__annotations__["a"] == int


def test_cache_thread_safety():
    call_count = 0

    @latency_cache(ttl_seconds=1.0)
    def heavy_task(x):
        nonlocal call_count
        time.sleep(0.05)
        call_count += 1
        return x

    import threading

    threads = [threading.Thread(target=heavy_task, args=(1,)) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert call_count == 1, "Race condition: Function executed multiple times"


def test_cache_isolation():
    @latency_cache(ttl_seconds=1.0)
    def func_a(x):
        return x

    @latency_cache(ttl_seconds=1.0)
    def func_b(x):
        return x + 1

    assert func_a(1) == 1
    assert func_b(1) == 2


def test_cache_multiple_keys():
    call_counts = {1: 0, 2: 0}

    @latency_cache(ttl_seconds=1.0)
    def compute(x):
        call_counts[x] += 1
        return x * 10

    assert compute(1) == 10
    assert compute(1) == 10
    assert compute(2) == 20
    assert compute(2) == 20
    assert call_counts[1] == 1
    assert call_counts[2] == 1


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - Use functools.wraps to handle metadata.
# - Use a dictionary to store (timestamp, value) tuples keyed by arguments.
# - Use a threading.Lock to wrap the calculation logic inside the wrapper.
