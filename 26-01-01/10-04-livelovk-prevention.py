import threading
import time

import pytest

"""
Implement a ResourceArbiter that negotiates exclusive access to a singleton resource.

Requirements:
1. The method `claim_leadership` must attempt to acquire the provided lock and return True when leadership is claimed.
2. If the lock is not available, `claim_leadership` must retry after a backoff period until a total timeout elapses.
3. The arbiter must expose a public integer attribute `collisions` counting failed acquisition attempts.
4. If leadership cannot be obtained before the timeout, `claim_leadership` must raise `ArbiterTimeoutError`.
"""


class ArbiterTimeoutError(Exception):
    pass


class ResourceArbiter:
    def __init__(self, shared_lock, timeout: float):
        raise NotImplementedError()

    def claim_leadership(self) -> bool:
        """Returns True if leadership claimed, raises ArbiterTimeoutError on timeout."""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_arbiter_single_claim():
    lock = threading.Lock()
    arbiter = ResourceArbiter(lock, timeout=1.0)
    assert arbiter.claim_leadership() is True
    assert lock.locked()


def test_arbiter_contention_resolution():
    lock = threading.Lock()
    results = []

    def worker(name):
        arbiter = ResourceArbiter(lock, timeout=2.0)
        try:
            if arbiter.claim_leadership():
                time.sleep(0.1)  # Hold for a bit
                lock.release()
                results.append(name)
        except ArbiterTimeoutError:
            results.append(f"{name}_failed")

    t1 = threading.Thread(target=worker, args=("A",))
    t2 = threading.Thread(target=worker, args=("B",))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert "A" in results
    assert "B" in results
    assert len(results) == 2


def test_arbiter_timeout():
    lock = threading.Lock()
    lock.acquire()  # Block it permanently

    arbiter = ResourceArbiter(lock, timeout=0.1)
    start = time.time()
    with pytest.raises(ArbiterTimeoutError):
        arbiter.claim_leadership()
    end = time.time()

    assert 0.1 <= (end - start) <= 0.2


def test_arbiter_random_backoff():
    # This test checks if multiple arbiters use different sleep durations
    lock = threading.Lock()
    lock.acquire()

    arbiter = ResourceArbiter(lock, timeout=0.5)

    # We monkeypatch time.sleep to record durations
    durations = []
    import time as real_time

    def mock_sleep(seconds):
        durations.append(seconds)
        real_time.sleep(0.001)

    import time

    original_sleep = time.sleep
    time.sleep = mock_sleep
    try:
        with pytest.raises(ArbiterTimeoutError):
            arbiter.claim_leadership()
    finally:
        time.sleep = original_sleep

    assert len(durations) > 1
    assert len(set(durations)) > 1, "Backoff durations were not randomized"


def test_collision_count_incremented():
    # If the lock is held permanently, collisions should be recorded before timeout
    lock = threading.Lock()
    lock.acquire()

    arbiter = ResourceArbiter(lock, timeout=0.1)
    with pytest.raises(ArbiterTimeoutError):
        arbiter.claim_leadership()

    # The arbiter should expose a collisions metric that increased during retries
    assert hasattr(arbiter, "collisions")
    assert arbiter.collisions > 0


if __name__ == "__main__":
    pytest.main([__file__])


# --- Hints (expand if stuck) ---
# - Use time.perf_counter() for accurate timeout tracking.
# - Use random.uniform(min, max) for the backoff.
# - Ensure the lock is acquired with blocking=False or a short timeout inside the loop.
