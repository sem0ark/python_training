import asyncio

import pytest

"""
Implement an AsyncScraper that concurrently fetches data from multiple sources.

Requirements:
1. `scrape_all` must execute requests concurrently and return a collection of per-request results.
2. The scraper must enforce a maximum concurrency bound (`max_concurrency`) so that at most that many requests run at the same time.
3. If an individual request exceeds the per-request `timeout`, that request must fail while allowing other requests to continue.
4. The scraper must not block the event loop while performing its work.
"""


class AsyncScraper:
    def __init__(self, max_concurrency: int, timeout: float):
        raise NotImplementedError()

    async def fetch_one(self, url: str):
        # Simulates an API call
        raise NotImplementedError()

    async def scrape_all(self, urls: list):
        raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


@pytest.mark.asyncio
async def test_scraper_concurrency_limit():
    scraper = AsyncScraper(max_concurrency=2, timeout=1.0)
    urls = ["url1", "url2", "url3", "url4"]

    start_time = asyncio.get_event_loop().time()
    # fetch_one is mocked to take 0.1s
    results = await scraper.scrape_all(urls)
    end_time = asyncio.get_event_loop().time()

    # If concurrency is 2, 4 urls should take ~0.2s (not 0.4s and not 0.1s)
    duration = end_time - start_time
    assert 0.18 <= duration <= 0.25
    assert len(results) == 4


@pytest.mark.asyncio
async def test_scrape_all_returns_all_items():
    scraper = AsyncScraper(max_concurrency=3, timeout=1.0)
    urls = [f"u{i}" for i in range(6)]
    results = await scraper.scrape_all(urls)
    assert len(results) == 6


@pytest.mark.asyncio
async def test_partial_failures_do_not_cancel_others():
    scraper = AsyncScraper(max_concurrency=2, timeout=0.05)
    urls = ["fast1", "slow_fail", "fast2"]
    results = await scraper.scrape_all(urls)
    # fast results present, slow_fail produced an error or None
    assert any("fast" in str(r) for r in results)


@pytest.mark.asyncio
async def test_scraper_timeout_handling():
    # Mocking behavior: "slow_url" takes 2 seconds
    scraper = AsyncScraper(max_concurrency=5, timeout=0.1)
    urls = ["fast_url", "slow_url"]

    results = await scraper.scrape_all(urls)

    # slow_url should have returned an Exception or None depending on implementation
    # but fast_url must succeed.
    assert "fast_url_data" in results
    assert any(
        isinstance(r, (asyncio.TimeoutError, Exception)) or r is None for r in results
    )


@pytest.mark.asyncio
async def test_scraper_no_loop_blocking():
    scraper = AsyncScraper(max_concurrency=1, timeout=1.0)

    async def heartbeat():
        count = 0
        for _ in range(10):
            await asyncio.sleep(0.01)
            count += 1
        return count

    # Run scraper and heartbeat together
    heartbeat_task = asyncio.create_task(heartbeat())
    await scraper.scrape_all(["url1", "url2"])

    count = await heartbeat_task
    assert count >= 9, "The event loop was blocked!"


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints (expand if stuck) ---
# - Use asyncio.Semaphore to control concurrency.
# - Use asyncio.wait_for to implement the per-request timeout.
# - Use asyncio.gather(..., return_exceptions=True) to handle partial failures.
