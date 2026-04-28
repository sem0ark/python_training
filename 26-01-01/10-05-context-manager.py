import threading

import pytest

"""
Implement a thread-safe AuditLedger that records financial transactions. 

Requirements:
1. Multiple threads must be able to append transactions simultaneously without data loss or corruption.
2. The ledger must provide a context manager interface for 'batch' entries.
3. If an exception occurs within a batch context, no entries from that batch should be committed to the final ledger.
4. The ledger must maintain a strictly monotonic record of entries.
"""


class AuditError(Exception):
    pass


class AuditLedger:
    def __init__(self):
        raise NotImplementedError()

    def add_entry(self, transaction_id: str):
        raise NotImplementedError()

    def batch(self):
        raise NotImplementedError()

    def __len__(self):
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_ledger_single_thread():
    ledger = AuditLedger()
    ledger.add_entry("TXN001")
    assert len(ledger) == 1


def test_ledger_batch_commit():
    ledger = AuditLedger()
    with ledger.batch():
        ledger.add_entry("TXN001")
        ledger.add_entry("TXN002")
    assert len(ledger) == 2


def test_ledger_batch_rollback():
    ledger = AuditLedger()
    try:
        with ledger.batch():
            ledger.add_entry("TXN001")
            raise ValueError("System Failure")
    except ValueError:
        pass

    assert len(ledger) == 0


def test_ledger_concurrency():
    ledger = AuditLedger()

    def worker(id_prefix):
        for i in range(100):
            ledger.add_entry(f"{id_prefix}_{i}")

    threads = [threading.Thread(target=worker, args=(f"T{i}",)) for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert len(ledger) == 1000


def test_ledger_isolation():
    ledger_a = AuditLedger()
    ledger_b = AuditLedger()
    ledger_a.add_entry("A1")
    assert len(ledger_b) == 0


if __name__ == "__main__":
    pytest.main([__file__])


# --- Hints (expand if stuck) ---
# - Use threading.Lock to protect the underlying storage.
# - For the batch rollback, use a temporary local list in the context manager and only merge it on __exit__ if no error occurred.
