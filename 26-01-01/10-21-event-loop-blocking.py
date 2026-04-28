import asyncio
import time

import pytest

"""
Scenario: A busy kitchen uses an event loop to manage orders.

Requirements:
1. `efficient_chef(id, duration)` must perform work without blocking the event loop for the specified duration.
2. `angry_chef(duration)` must perform a blocking operation that prevents the event loop from scheduling other tasks for the specified duration.
3. Implement `kitchen_monitor()`: A coroutine that runs in the background and 
   increments a counter every 0.1s to track loop responsiveness.
4. Tests will demonstrate that a blocking operation prevents the monitor from making progress while non-blocking work does not.
"""


class Restaurant:
    def __init__(self):
        self.monitor_ticks = 0
        self.stop_monitor = False

    async def kitchen_monitor(self):
        """Increments self.monitor_ticks every 0.1 seconds."""
        raise NotImplementedError()

    async def efficient_chef(self, duration: float):
        """Simulates non-blocking work."""
        raise NotImplementedError()

    def angry_chef(self, duration: float):
        """Simulates blocking work using synchronous sleep."""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


@pytest.mark.asyncio
async def test_loop_starvation():
    rest = Restaurant()

    # Start the monitor in the background
    monitor_task = asyncio.create_task(rest.kitchen_monitor())

    # Allow monitor to run for a bit
    await asyncio.sleep(0.2)
    ticks_before = rest.monitor_ticks
    assert ticks_before > 0, "Monitor should be ticking"

    # Run efficient chef (non-blocking)
    await rest.efficient_chef(0.3)
    ticks_after_efficient = rest.monitor_ticks
    assert ticks_after_efficient > ticks_before, (
        "Monitor should continue during efficient chef"
    )

    # Run angry chef (blocking)
    # Note: We call it inside the loop to see the effect
    start_time = asyncio.get_event_loop().time()
    rest.angry_chef(0.5)
    end_time = asyncio.get_event_loop().time()

    ticks_after_angry = rest.monitor_ticks

    # Verification
    assert (end_time - start_time) >= 0.5
    assert ticks_after_angry == ticks_after_efficient, (
        f"Monitor starved! Expected {ticks_after_efficient} ticks, got {ticks_after_angry}. "
        "The loop was blocked, so the monitor task could not run."
    )

    rest.stop_monitor = True
    await monitor_task


@pytest.mark.asyncio
async def test_monitor_stop_flag():
    rest = Restaurant()
    monitor_task = asyncio.create_task(rest.kitchen_monitor())
    await asyncio.sleep(0.15)
    rest.stop_monitor = True
    await monitor_task
    # After stopping, monitor should not be running and ticks should be non-negative
    assert rest.monitor_ticks >= 0


@pytest.mark.asyncio
async def test_efficient_chef_keeps_loop_responsive():
    rest = Restaurant()
    monitor = asyncio.create_task(rest.kitchen_monitor())
    await asyncio.sleep(0.05)
    before = rest.monitor_ticks
    await rest.efficient_chef(0.2)
    after = rest.monitor_ticks
    rest.stop_monitor = True
    await monitor
    assert after > before


@pytest.mark.asyncio
async def test_concurrency_impact():
    rest = Restaurant()

    # If we run two efficient chefs, they should run concurrently
    start = time.perf_counter()
    await asyncio.gather(rest.efficient_chef(0.2), rest.efficient_chef(0.2))
    duration = time.perf_counter() - start

    assert duration < 0.35, "Efficient chefs should run concurrently"


if __name__ == "__main__":
    pytest.main([__file__])


# --- Hints ---
# - Use asyncio.sleep() for non-blocking and time.sleep() for blocking.
# - Remember that the Event Loop is single-threaded; if one function doesn't 'await',
#   nothing else can happen.
