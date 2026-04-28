import multiprocessing

import pytest

"""
Implement a ProcessVault that provides a dictionary-like secret store accessible from multiple OS processes.

Requirements:
1. Secrets written in one process must be observable by other processes using the same vault instance.
2. Concurrent access must be process-safe: simultaneous writers must not corrupt stored values.
3. Operations on one vault instance must not affect another vault instance.
4. Attempts to store non-serializable values must raise a VaultError (not an uncaught system exception).
"""


class VaultError(Exception):
    pass


class ProcessVault:
    def __init__(self):
        raise NotImplementedError()

    def set_secret(self, key: str, value: str):
        raise NotImplementedError()

    def get_secret(self, key: str):
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def _worker_set(vault, key, val):
    vault.set_secret(key, val)


def _worker_get(vault, key, queue):
    queue.put(vault.get_secret(key))


def test_vault_cross_process():
    vault = ProcessVault()
    p = multiprocessing.Process(
        target=_worker_set, args=(vault, "api_key", "secret123")
    )
    p.start()
    p.join()

    assert vault.get_secret("api_key") == "secret123"


def test_vault_concurrency():
    vault = ProcessVault()

    def run_updates():
        for i in range(50):
            vault.set_secret(f"key_{i}", "val")

    processes = [multiprocessing.Process(target=run_updates) for _ in range(4)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()

    # Check if all keys exist (ensures no overwrites/corruption)
    for i in range(50):
        assert vault.get_secret(f"key_{i}") == "val"


def test_vault_serialization_error():
    vault = ProcessVault()
    with pytest.raises(VaultError):
        # Functions are generally not picklable in a way that works here
        vault.set_secret("fail", lambda x: x)


def test_vault_isolation():
    v1 = ProcessVault()
    v2 = ProcessVault()
    v1.set_secret("k", "v1")
    v2.set_secret("k", "v2")
    assert v1.get_secret("k") == "v1"
    assert v2.get_secret("k") == "v2"


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - Explore multiprocessing.Manager to create a shared dict.
# - Use a multiprocessing.Lock to ensure write atomicity if the manager's dict isn't enough for your logic.
