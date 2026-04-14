"""
Layered Logger (Inheritance & super())
- Use super() to extend a base class's functionality.
- FilteredLogger should only log messages that don't contain "SECRET".
"""

import pytest


class BaseLogger:
    def __init__(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)


class FilteredLogger(BaseLogger):
    """
    Requirements:
    1. Override `log(message)`.
    2. If "SECRET" is in the message, do nothing.
    3. Otherwise, use super() to call the original log method.
    """


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_filtered_logger():
    logger = FilteredLogger()
    logger.log("Hello World")
    logger.log("This is a SECRET message")

    assert "Hello World" in logger.logs
    assert "This is a SECRET message" not in logger.logs
    assert len(logger.logs) == 1


def test_logger_allowed():
    f = FilteredLogger()
    f.log("Public info")
    assert "Public info" in f.logs


def test_logger_filtered():
    f = FilteredLogger()
    f.log("This is a SECRET")
    assert len(f.logs) == 0


def test_logger_multiple_messages():
    f = FilteredLogger()
    f.log("One")
    f.log("Two SECRET")
    f.log("Three")
    assert f.logs == ["One", "Three"]


def test_logger_inheritance_check():
    f = FilteredLogger()
    assert isinstance(f, BaseLogger)


def test_logger_empty_message():
    f = FilteredLogger()
    f.log("")
    assert f.logs == [""]


if __name__ == "__main__":
    pytest.main([__file__])
