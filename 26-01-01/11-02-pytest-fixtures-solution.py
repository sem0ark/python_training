import time

import pytest

"""
The following infrastructure management suite contains configuration errors affecting 
test collection, state isolation, and execution performance.

Requirements:
1. The `global_config` fixture must provide a `CloudConfig` instance initialized with the value from the `user_token` fixture.
2. The `global_config` fixture must be instantiated exactly once for the entire test session.
3. Every test receiving the `shared_data_cache` fixture must receive a fresh, empty list. 
4. Mutations to the list provided by `shared_data_cache` must not persist between different test functions.
5. The `heavy_analytics_logger` fixture must only execute when a test explicitly includes it in its arguments.
6. The total wall-clock time for the test suite must be less than 1.0 second.

Concepts: Fixture scope hierarchy, mutable state isolation, execution side-effects
"""

# ---------------------------------------------------------------------------
# System under test
# ---------------------------------------------------------------------------


class CloudConfig:
    def __init__(self, admin_token: str):
        self.admin_token = admin_token
        self.is_loaded = True


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def user_token() -> str:
    """Fixture providing a mock user token with session scope."""
    return "SECRET_TOKEN_123"


@pytest.fixture(scope="session")
def global_config(user_token: str) -> CloudConfig:
    """Fixture providing a CloudConfig instance initialized once per session."""
    return CloudConfig(user_token)


@pytest.fixture(scope="function")
def shared_data_cache() -> list[str]:
    """Fixture providing a fresh, isolated list for each test."""
    return []


@pytest.fixture
def heavy_analytics_logger() -> str:
    """Mock logger fixture with reduced sleep to meet performance constraints."""
    # Reduced from 1.0 to stay within the < 1.0s suite limit.
    time.sleep(0.01)
    return "logged"


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_config_initialization(global_config):
    assert isinstance(global_config, CloudConfig)
    assert global_config.is_loaded is True
    assert global_config.admin_token == "SECRET_TOKEN_123"


def test_cache_isolation_part_one(shared_data_cache):
    shared_data_cache.append("session_data_alpha")
    assert len(shared_data_cache) == 1


def test_cache_isolation_part_two(shared_data_cache):
    assert len(shared_data_cache) == 0


def test_logger_explicit_invocation(heavy_analytics_logger):
    assert heavy_analytics_logger == "logged"


def test_suite_performance_constraint():
    start = time.monotonic()
    _ = [x**2 for x in range(1000)]
    elapsed = time.monotonic() - start
    assert elapsed < 0.1


def test_config_session_persistence(global_config):
    if not hasattr(test_config_session_persistence, "_first_id"):
        test_config_session_persistence._first_id = id(global_config)

    assert id(global_config) == test_config_session_persistence._first_id


@pytest.mark.parametrize("iteration", range(3))
def test_rapid_execution_boundary(iteration):
    assert True


if __name__ == "__main__":
    start_time = time.monotonic()
    exit_code = pytest.main([__file__, "-v"])
    total_time = time.monotonic() - start_time

    if total_time >= 1.0:
        print(f"\nPERFORMANCE FAILURE: Suite took {total_time:.2f}s")
        exit(1)
    else:
        print(f"\nPERFORMANCE SUCCESS: Suite took {total_time:.2f}s")
        exit(exit_code)


# --- Hints (expand if stuck) ---
# - Pytest fixtures have a 'scope' parameter: "function", "class", "module", "package", or "session".
# - A fixture with a broader scope (e.g., session) cannot depend on a fixture with a narrower scope (e.g., function).
# - By default, fixtures are function-scoped.
# - If a fixture is running when it isn't requested, check its 'autouse' parameter.
# - To ensure a list is fresh for every test, consider which scope generates a new object for every calling function.
