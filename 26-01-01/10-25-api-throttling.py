import asyncio

import pytest

"""
Implement a high-concurrency scraper that enforces a limit on simultaneous outbound requests.

Requirements:
1. `fetch(url)` must increment an active-connection counter while a request runs and decrement it when finished.
2. If the number of active connections equals the configured limit, new fetches must wait until a slot frees up.
3. If a fetch raises an exception, its connection slot must be released so other requests can proceed.
4. `run_batch(urls)` must schedule all fetches and wait for completion while respecting the concurrency bound.
"""


class Scraper:
    def __init__(self, connection_limit: int):
        self.limit = connection_limit
        self.active_count = 0
        self.max_observed_active = 0
        raise NotImplementedError()

    async def fetch(self, url: str):
        """
        Simulates fetching a URL.
        Increments active_count, sleeps briefly, then decrements.
        Must use the semaphore to throttle.
        """
        raise NotImplementedError()

    async def run_batch(self, urls: list):
        """Schedules all fetches and waits for completion."""
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


@pytest.mark.asyncio
async def test_semaphore_throttling_limit():
    limit = 5
    scraper = Scraper(limit)
    urls = [f"http://api.com/{i}" for i in range(20)]

    await scraper.run_batch(urls)

    # The active count should never have exceeded the limit
    assert scraper.max_observed_active <= limit
    assert scraper.active_count == 0


@pytest.mark.asyncio
async def test_semaphore_resilience_on_failure():
    limit = 2
    scraper = Scraper(limit)

    async def failing_fetch(url):
        async with scraper._semaphore:  # Accessing internal for test setup
            scraper.active_count += 1
            raise RuntimeError("Network Crash")

    # If the semaphore isn't released on failure, the loop will hang
    try:
        await asyncio.wait_for(scraper.fetch("http://fail.com"), timeout=0.1)
    except (RuntimeError, asyncio.TimeoutError):
        pass

    # Slot should be free now
    assert scraper._semaphore.locked() is False


@pytest.mark.asyncio
async def test_concurrency_execution():
    scraper = Scraper(10)
    urls = [f"url_{i}" for i in range(10)]

    start = asyncio.get_event_loop().time()
    await scraper.run_batch(urls)
    end = asyncio.get_event_loop().time()

    # Since fetch has a simulated delay (e.g. 0.05s),
    # running 10 concurrently should take ~0.05s, not 0.5s.
    assert (end - start) < 0.2


@pytest.mark.asyncio
async def test_active_count_and_max_observed():
    scraper = Scraper(3)
    urls = [f"u{i}" for i in range(6)]
    await scraper.run_batch(urls)
    assert scraper.active_count == 0
    assert scraper.max_observed_active <= 3


@pytest.mark.asyncio
async def test_slot_release_on_success_and_failure():
    s = Scraper(2)
    # Run batch where one fetch may raise; after completion slots should be free
    try:
        await asyncio.wait_for(s.fetch("ok://"), timeout=0.2)
    except Exception:
        pass
    assert s._semaphore.locked() is False


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - Use `asyncio.Semaphore` as an asynchronous context manager.
# - To track `max_observed_active`, update it inside the critical section.
