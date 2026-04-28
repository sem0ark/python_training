import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

"""
Bridge a legacy synchronous data-cruncher into an async pipeline without blocking the event loop.

Requirements:
1. `legacy_cruncher(data)` must be a synchronous, blocking function that simulates work.
2. `AsyncBridge.calculate(data)` must offload the blocking work to a thread pool and return an awaitable that resolves to the result.
3. The event loop must remain responsive while calculations run via the bridge.
4. Concurrent calls to `calculate` must be able to run in parallel if the executor has multiple workers.
"""


def legacy_cruncher(data: int) -> int:
    """Synchronous, blocking function."""
    time.sleep(0.5)
    return data * 2


class AsyncBridge:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.loop_was_blocked = False

    async def calculate(self, data: int) -> int:
        """Runs legacy_cruncher in the executor without blocking the loop."""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


@pytest.mark.asyncio
async def test_loop_responsiveness_during_calculation():
    bridge = AsyncBridge()

    heartbeat_count = 0

    async def heartbeat():
        nonlocal heartbeat_count
        while True:
            await asyncio.sleep(0.1)
            heartbeat_count += 1

    # Start a background task to prove the loop is moving
    hb_task = asyncio.create_task(heartbeat())

    # Run the blocking calculation through the bridge
    start_time = asyncio.get_event_loop().time()
    result = await bridge.calculate(21)
    end_time = asyncio.get_event_loop().time()

    hb_task.cancel()

    assert result == 42
    assert (end_time - start_time) >= 0.5
    # If the loop was blocked, heartbeat_count would be 0 or 1.
    # If non-blocking, it should be ~5.
    assert heartbeat_count >= 3, "The Event Loop was blocked by the legacy cruncher!"


@pytest.mark.asyncio
async def test_calculate_is_awaitable():
    bridge = AsyncBridge()
    coro = bridge.calculate(5)
    import inspect

    assert inspect.isawaitable(coro)
    result = await coro
    assert result == 10


@pytest.mark.asyncio
async def test_sequential_when_single_worker():
    bridge = AsyncBridge()
    bridge.executor = ThreadPoolExecutor(max_workers=1)

    start = asyncio.get_event_loop().time()
    res = await asyncio.gather(bridge.calculate(1), bridge.calculate(2))
    end = asyncio.get_event_loop().time()
    assert res == [2, 4]
    # With single worker, two 0.5s tasks should take at least ~1.0s
    assert (end - start) >= 0.9


@pytest.mark.asyncio
async def test_multiple_concurrent_bridge_calls():
    bridge = AsyncBridge()
    # Increase workers for this test
    bridge.executor = ThreadPoolExecutor(max_workers=2)

    start = asyncio.get_event_loop().time()
    results = await asyncio.gather(bridge.calculate(10), bridge.calculate(20))
    end = asyncio.get_event_loop().time()

    assert results == [20, 40]
    # Should take ~0.5s if parallel in threads, not 1.0s
    assert (end - start) < 0.8


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - Use `loop.run_in_executor(executor, func, *args)`.
# - Use `asyncio.get_running_loop()` to get the current loop.
