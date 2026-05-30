import os
import shutil
import tempfile
from typing import Generator

import pytest

"""
The following test infrastructure contains incomplete fixture definitions that affect
test execution, resource management, and test isolation.

Requirements:
1. The `temp_workspace` fixture must automatically initialize a temporary directory before ANY test runs, without being explicitly requested by tests.
2. The `temp_workspace` fixture must provide the path to this temporary directory.
3. An environment variable `TEST_WORKSPACE_PATH` must be set to the temp directory path before any test executes, and must be available to all tests.
4. The `temp_workspace` fixture must clean up (remove) the temporary directory after all tests complete.
5. Every test that uses `temp_workspace` must receive a fresh, empty temporary directory.
6. The `database_connection` fixture must only initialize when explicitly requested by a test.
7. Tests must be able to write files to the workspace and read them back correctly.
8. The cleanup must occur exactly once per test session, not per test function.

Concepts: Fixture autouse, scope hierarchy, setup/teardown, environment side-effects, resource management.
"""

# ---------------------------------------------------------------------------
# System under test
# ---------------------------------------------------------------------------


class DatabaseConnection:
    """Expensive resource that should only be created when needed."""

    def __init__(self):
        self.is_connected = True
        self.query_count = 0

    def execute_query(self, query: str):
        self.query_count += 1
        return f"Result for: {query}"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def root_temp_dir() -> Generator[str, None, None]:
    """Session-scoped root directory to ensure exactly one cleanup."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture(autouse=True)
def temp_workspace(root_temp_dir: str) -> Generator[str, None, None]:
    """
    Function-scoped workspace that provides isolation for each test.
    Automatically runs, sets environment variables, and provides a fresh path.
    """
    # Create a unique sub-directory for this test function
    test_workspace = tempfile.mkdtemp(dir=root_temp_dir)
    os.environ["TEST_WORKSPACE_PATH"] = test_workspace
    yield test_workspace
    # We don't necessarily need to remove the sub-dir here since the
    # root_temp_dir will be removed at the end of the session,
    # satisfying the 'exactly once per session' cleanup requirement.


@pytest.fixture
def database_connection() -> DatabaseConnection:
    """
    Initializes only when explicitly requested by a test.
    """
    return DatabaseConnection()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_workspace_exists(temp_workspace):
    """Verify the workspace directory exists and is accessible."""
    assert os.path.isdir(temp_workspace)
    assert os.path.exists(temp_workspace)


def test_workspace_env_var_set():
    """Verify TEST_WORKSPACE_PATH environment variable is set."""
    assert "TEST_WORKSPACE_PATH" in os.environ
    workspace_path = os.environ["TEST_WORKSPACE_PATH"]
    assert os.path.isdir(workspace_path)


def test_workspace_isolation_part_one(temp_workspace):
    """Write a file to the workspace."""
    test_file = os.path.join(temp_workspace, "test_data.txt")
    with open(test_file, "w") as f:
        f.write("data_from_test_one")
    assert os.path.exists(test_file)


def test_workspace_isolation_part_two(temp_workspace):
    """Verify the workspace is fresh (file from previous test doesn't exist)."""
    test_file = os.path.join(temp_workspace, "test_data.txt")
    assert not os.path.exists(test_file), "Workspace should be isolated per test"

    # Write a different file
    new_file = os.path.join(temp_workspace, "test_data_two.txt")
    with open(new_file, "w") as f:
        f.write("data_from_test_two")
    assert os.path.exists(new_file)


def test_database_not_initialized_automatically():
    """
    Verify that database_connection fixture does NOT run automatically.
    This test does NOT request the database_connection fixture.
    If it ran automatically, this test would fail due to resource initialization.
    """
    # This test should pass without initializing the database
    assert True


def test_database_explicit_initialization(database_connection):
    """
    Verify that database_connection only initializes when explicitly requested.
    """
    assert isinstance(database_connection, DatabaseConnection)
    assert database_connection.is_connected is True


def test_database_query_execution(database_connection):
    """Verify the database connection can execute queries."""
    result = database_connection.execute_query("SELECT * FROM users")
    assert "Result for:" in result
    assert database_connection.query_count == 1


def test_workspace_file_operations(temp_workspace):
    """Verify we can perform file operations in the workspace."""
    test_file = os.path.join(temp_workspace, "operations.txt")

    # Write
    with open(test_file, "w") as f:
        f.write("test content")

    # Read
    with open(test_file, "r") as f:
        content = f.read()

    assert content == "test content"


@pytest.mark.parametrize("file_num", range(3))
def test_workspace_multiple_files(temp_workspace, file_num):
    """Verify multiple tests can create files without interference."""
    test_file = os.path.join(temp_workspace, f"file_{file_num}.txt")
    with open(test_file, "w") as f:
        f.write(f"content_{file_num}")
    assert os.path.exists(test_file)


if __name__ == "__main__":
    exit_code = pytest.main([__file__, "-v"])
    exit(exit_code)


# --- Hints (expand if stuck) ---
# - Use @pytest.fixture(autouse=True) to make a fixture run automatically.
# - Use scope="session" for setup/teardown that should happen once per test session.
# - Use scope="function" for setup/teardown that should happen per test function.
# - Use tempfile.mkdtemp() to create a temporary directory.
# - Use os.environ to set environment variables.
# - Use yield in fixtures to separate setup (before yield) from teardown (after yield).
# - Be careful: autouse fixtures with function scope run before EVERY test.
# - A session-scoped autouse fixture runs once at the start of the session.
