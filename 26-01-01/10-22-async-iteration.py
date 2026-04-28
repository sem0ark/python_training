import asyncio

import pytest

"""
Scenario: You are building a data pipeline for a "Deep Space Archive." 
The archive is massive, and fetching every record at once would crash the system. 
You must implement a memory-efficient Async Iterator that fetches records one by one.

Requirements:
1. Implement `ArchiveCursor`: A class that accepts a list of `data` and a `delay`.
2. Must implement the Asynchronous Iterator protocol (`__aiter__` and `__anext__`).
3. Every iteration (fetch) must simulate I/O latency using the provided `delay`.
4. The cursor must maintain internal state to track its position.
5. When all records are exhausted, it must raise the correct asynchronous signal to stop the loop.

Also implement a function-based asynchronous generator `archive_streamer` that provides the same behavior.
"""


class ArchiveCursor:
    def __init__(self, data: list, delay: float):
        raise NotImplementedError()

    def __aiter__(self):
        raise NotImplementedError()

    async def __anext__(self):
        raise NotImplementedError()


async def archive_streamer(data: list, delay: float):
    """
    Asynchronous generator that yields records with a delay.
    """
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


@pytest.mark.asyncio
async def test_iterator_protocol_compliance():
    data = ["Signal A", "Signal B", "Signal C"]
    cursor = ArchiveCursor(data, 0.01)

    results = []
    async for record in cursor:
        results.append(record)

    assert results == data
    assert len(results) == 3


@pytest.mark.asyncio
async def test_iterator_is_non_blocking():
    # This test ensures the iterator yields control back to the loop
    # while it is "waiting" for a record.
    data = [f"Record {i}" for i in range(5)]
    cursor = ArchiveCursor(data, 0.1)

    background_counter = 0

    async def incrementer():
        nonlocal background_counter
        for _ in range(5):
            await asyncio.sleep(0.05)
            background_counter += 1

    # Run the iterator and the background task concurrently
    counter_task = asyncio.create_task(incrementer())

    results = []
    async for record in cursor:
        results.append(record)

    await counter_task

    assert len(results) == 5
    assert background_counter > 0, "The loop was blocked! Background task couldn't run."


@pytest.mark.asyncio
async def test_empty_archive():
    cursor = ArchiveCursor([], 0.01)
    results = []
    async for record in cursor:
        results.append(record)
    assert results == []


@pytest.mark.asyncio
async def test_manual_anext_exception():
    cursor = ArchiveCursor(["One"], 0.01)
    await cursor.__anext__()
    with pytest.raises(StopAsyncIteration):
        await cursor.__anext__()


# --- DO NOT MODIFY THE TESTS BELOW ---


@pytest.mark.asyncio
async def test_streamer_basic_yield():
    data = ["Galaxy A", "Galaxy B", "Nebula X"]
    stream = archive_streamer(data, 0.01)

    results = []
    async for record in stream:
        results.append(record)

    assert results == data
    assert len(results) == 3


@pytest.mark.asyncio
async def test_streamer_is_non_blocking():
    # This test ensures the generator yields control to the loop during sleeps.
    data = [f"Star {i}" for i in range(3)]
    delay = 0.1

    background_tasks_completed = 0

    async def quick_task():
        nonlocal background_tasks_completed
        while True:
            await asyncio.sleep(0.02)
            background_tasks_completed += 1

    # Start a background task
    bg_monitor = asyncio.create_task(quick_task())

    results = []
    async for record in archive_streamer(data, delay):
        results.append(record)

    bg_monitor.cancel()

    assert len(results) == 3
    # If the generator was blocking (e.g. using time.sleep),
    # the background task would never have a chance to run.
    assert background_tasks_completed >= 5


@pytest.mark.asyncio
async def test_streamer_empty_data():
    stream = archive_streamer([], 0.01)
    results = []
    async for record in stream:
        results.append(record)
    assert results == []


@pytest.mark.asyncio
async def test_streamer_manual_iteration():
    data = ["Signal"]
    gen = archive_streamer(data, 0.01)

    # Manually get the first item
    first = await gen.__anext__()
    assert first == "Signal"

    # The next call should raise StopAsyncIteration
    with pytest.raises(StopAsyncIteration):
        await gen.__anext__()


@pytest.mark.asyncio
async def test_streamer_type_contract():
    gen = archive_streamer(["data"], 0.1)
    # Verify it is an asynchronous generator object
    import inspect

    assert inspect.isasyncgen(gen)
    # Clean up
    async for _ in gen:
        pass


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - __aiter__ should return the iterator object itself (usually 'self').
# - __anext__ is a coroutine; it must use 'await' for the delay.
# - To signal the end of an async for loop, raise StopAsyncIteration (not StopIteration).
# - Use 'async def' combined with 'yield' to create an async generator.
# - Use 'await asyncio.sleep(delay)' to simulate the non-blocking fetch.
# - Async generators automatically handle 'StopAsyncIteration' when the function returns.
