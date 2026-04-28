import threading
import time

import pytest

"""
Implement a TimeoutLock that prevents indefinite blocking.

Requirements:
1. The lock must support a context manager interface.
2. If the lock cannot be acquired within the specified 'timeout', it must raise a 'LockAcquisitionError'.
3. The 'LockAcquisitionError' must explicitly chain the original timeout cause if applicable.
4. If an acquisition fails, it must not leave the lock in a corrupted or "held" state.
"""


class LockAcquisitionError(Exception):
    pass


class TimeoutLock:
    def __init__(self, timeout: float):
        raise NotImplementedError()

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_lock_basic_acquisition():
    lock = TimeoutLock(timeout=0.1)
    with lock:
        assert True


def test_lock_timeout_raises():
    lock = TimeoutLock(timeout=0.05)

    def hold_lock():
        with lock:
            time.sleep(0.2)

    t = threading.Thread(target=hold_lock)
    t.start()
    time.sleep(0.01)  # Ensure thread grabs lock

    with pytest.raises(LockAcquisitionError) as exc_info:
        with lock:
            pass

    assert "could not be acquired" in str(exc_info.value)
    t.join()


def test_lock_exception_chaining():
    lock = TimeoutLock(timeout=0.01)
    # Lock it manually to force a timeout
    inner_lock = threading.Lock()
    inner_lock.acquire()

    # We simulate the internal lock being held
    lock._lock = inner_lock

    with pytest.raises(LockAcquisitionError) as exc_info:
        with lock:
            pass

    # Verification of error contract
    assert exc_info.value.__suppress_context__ is False


def test_lock_reusability():
    lock = TimeoutLock(timeout=0.1)
    with lock:
        pass
    with lock:
        pass  # Should work immediately


def test_lock_chains_cause():
    lock = TimeoutLock(timeout=0.01)
    # Simulate internal lock that causes acquire to fail
    inner_lock = threading.Lock()
    inner_lock.acquire()
    lock._lock = inner_lock

    with pytest.raises(LockAcquisitionError) as exc_info:
        with lock:
            pass

    # The raised LockAcquisitionError should chain the original timeout cause
    assert exc_info.value.__cause__ is not None
    assert "could not be acquired" in str(exc_info.value)


def test_multiple_locks_independent():
    # Two different TimeoutLock instances should be independent and reusable
    l1 = TimeoutLock(timeout=0.1)
    l2 = TimeoutLock(timeout=0.1)
    with l1:
        with l2:
            assert True


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - Use the 'blocking' and 'timeout' arguments of the standard threading.Lock.acquire() method.
# - Ensure __exit__ only releases the lock if it was successfully acquired in __enter__.
