from datetime import datetime

import pytest
import requests

"""
Three services make calls to external systems: an HTTP API, the system clock,
and the file system. The services are already implemented. Your task is to
implement three fixtures that intercept those external calls so the tests run
without network access, without touching the clock, and without writing to disk.

The third-party API really does expect you to mock it - it charges per request.

Requirements:
1. `mock_api_service` must intercept outbound HTTP GET requests made by `UserService.fetch_user` and return a controlled response with `status_code` equal to 200 and a `json()` method whose return value contains at least `"id"`, `"name"`, and `"email"` keys. The `"id"` value must reflect the `user_id` passed to the call.
2. No real network request may occur in any test that uses `mock_api_service`.
3. `mock_system_time` must cause every call to `datetime.now()` within the test to return the fixed timestamp 2024-01-15 10:30:00. The returned value must be identical across multiple calls within the same test.
4. `mock_file_operations` must prevent any write from reaching the file system. It must also supply a readable mock file object so that `FileLogger.read_log` returns a list without raising an error.
5. All patches applied by each fixture must be fully reverted after the test that requested the fixture completes. Tests that do not request a fixture must not be affected by patches applied in other tests.
"""


# ---------------------------------------------------------------------------
# System under test
# ---------------------------------------------------------------------------


class UserService:
    @staticmethod
    def fetch_user(user_id: int):
        response = requests.get(f"https://api.example.com/users/{user_id}")
        return response.json()


class TimeTracker:
    @staticmethod
    def get_current_time():
        return datetime.now()

    @staticmethod
    def is_business_hours():
        current = datetime.now()
        return 9 <= current.hour < 17


class FileLogger:
    @staticmethod
    def log_event(filename: str, event: str):
        with open(filename, "a") as f:
            f.write(f"{datetime.now()}: {event}\n")
        return True

    @staticmethod
    def read_log(filename: str):
        with open(filename, "r") as f:
            return f.readlines()


# ---------------------------------------------------------------------------
# Fixtures - implement these
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_api_service(monkeypatch):
    raise NotImplementedError()


@pytest.fixture
def mock_system_time(monkeypatch):
    raise NotImplementedError()


@pytest.fixture
def mock_file_operations(monkeypatch):
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_fetch_user_returns_controlled_data(mock_api_service):
    user = UserService.fetch_user(user_id=42)
    assert user["id"] == 42
    assert user["name"] == "John Doe"
    assert user["email"] == "john@example.com"


def test_fetch_multiple_users_same_mock(mock_api_service):
    user_1 = UserService.fetch_user(user_id=1)
    user_2 = UserService.fetch_user(user_id=2)
    assert user_1["id"] == 1
    assert user_2["id"] == 2
    assert user_1["name"] == "John Doe"


def test_fixed_time_is_consistent_across_calls(mock_system_time):
    time_1 = TimeTracker.get_current_time()
    time_2 = TimeTracker.get_current_time()
    assert time_1 == time_2
    assert time_1.year == 2024
    assert time_1.month == 1
    assert time_1.day == 15
    assert time_1.hour == 10
    assert time_1.minute == 30


def test_business_hours_with_fixed_time(mock_system_time):
    assert TimeTracker.is_business_hours() is True


def test_file_log_event_does_not_write_to_disk(mock_file_operations):
    result = FileLogger.log_event("test.log", "Test event")
    assert result is True


def test_file_read_log_returns_list(mock_file_operations):
    lines = FileLogger.read_log("test.log")
    assert isinstance(lines, list)


def test_api_mock_reverted_between_tests_first(mock_api_service):
    user = UserService.fetch_user(user_id=100)
    assert user["id"] == 100


def test_api_mock_reverted_between_tests_second(mock_api_service):
    user = UserService.fetch_user(user_id=200)
    assert user["id"] == 200


def test_api_and_time_mocks_compose(mock_api_service, mock_system_time):
    user = UserService.fetch_user(user_id=99)
    current_time = TimeTracker.get_current_time()
    assert user["id"] == 99
    assert current_time.hour == 10


def test_time_and_file_mocks_compose(mock_system_time, mock_file_operations):
    current_time = TimeTracker.get_current_time()
    result = FileLogger.log_event("combined.log", "Combined test")
    assert current_time.year == 2024
    assert result is True


def test_unmocked_time_is_real_datetime(mock_api_service):
    user = UserService.fetch_user(user_id=50)
    assert user["id"] == 50
    real_time = TimeTracker.get_current_time()
    assert isinstance(real_time, datetime)


@pytest.mark.parametrize("user_id", [10, 20, 30])
def test_parametrized_fetch_user(mock_api_service, user_id):
    user = UserService.fetch_user(user_id=user_id)
    assert user["id"] == user_id


@pytest.mark.skip(reason="Requires real network access")
def test_real_api_without_mock():
    user = UserService.fetch_user(user_id=1)
    assert "id" in user


if __name__ == "__main__":
    exit_code = pytest.main([__file__, "-v"])
    exit(exit_code)


# --- Hints (expand if stuck) ---
# - `monkeypatch.setattr(target_module, "attribute_name", replacement)` replaces an attribute on a module for the duration of the test.
# - Patch the name as it is *looked up* in the module that uses it, not where it is defined - e.g. patch `requests.get` where `requests` is imported.
# - `unittest.mock.Mock` and `unittest.mock.mock_open` (stdlib) can stand in for objects that need callable attributes or file-like behaviour.
# - `monkeypatch` reverts all patches automatically at test teardown; no explicit cleanup is needed inside the fixture.
# - For `datetime.now`, consider what object the module under test calls it on and patch at that location.
