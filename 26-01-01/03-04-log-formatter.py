import pytest

"""
Goal: Implement a professional-grade log formatter and a corresponding parser.

Requirements:
1. Implement `format_log(level, message, log_id, width=10)`:
   - Input Cleaning: Remove any leading/trailing whitespace from `level` and `message`.
   - Validation: If `level` contains non-alphabetic characters, raise a ValueError.
   - Level Formatting: Convert to UPPERCASE and center it within brackets `[]`.
   - Sanitization: Replace any occurrence of the word "password" (case-insensitive) 
     with "********".
   - Message Formatting: The message should be "Sentence capitalized" (only first 
     letter of the string uppercase).
   - Suffixing: Ensure the message ends with a single period `.`. Do not add a 
     duplicate if one already exists.
   - ID Padding: The `log_id` should be converted to a string and zero-padded 
     to be exactly 5 digits long (e.g., 42 -> "00042").
   - Final Structure: "ID | [  LEVEL  ] | Message."

2. Implement `is_critical(log_string)`:
   - Return True if the log level is "ERROR" or "CRITICAL".

3. Implement `parse_log(log_string)`:
   - Extract the level and the message from a formatted log string.
   - Hint: Use `partition`, `split`, or `find`/`index` with slicing.

Concepts: strip(), isalpha(), upper(), center(), replace(), capitalize(), 
          endswith(), zfill(), find(), partition(), __contains__.
"""


def format_log(level, message, log_id, width=10):
    # TODO: Implement the complex formatter
    raise NotImplementedError()


def is_critical(log_string):
    # TODO: Check for ERROR or CRITICAL levels
    raise NotImplementedError()


def parse_log(log_string):
    # TODO: Return a tuple of (level, message)
    # Example: ("00001 | [  INFO  ] | Hello.") -> ("INFO", "Hello.")
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_format_log_complex():
    # Test cleaning, casing, centering, padding, and suffixing
    log = format_log("  info  ", " system failure detected", 7, width=8)
    # ID (00007) | Level (centered in 8+2) | Message (Capitalized + .)
    assert log.startswith("00007")
    assert "[  INFO  ]" in log
    assert "System failure detected." in log


def test_sanitization():
    # Test case-insensitive replacement
    log = format_log("warn", "User entered Password123", 101)
    assert "Password" not in log
    assert "********123" in log


def test_validation_error():
    # Test isalpha() validation
    with pytest.raises(ValueError):
        format_log("L3V3L", "message", 1)


def test_suffix_logic():
    # Ensure we don't get double periods
    log = format_log("info", "Already has a period.", 1)
    assert log.endswith("Already has a period.")
    assert not log.endswith("..")


def test_is_critical():
    assert is_critical("00001 | [  ERROR  ] | Disk full.") is True
    assert is_critical("00002 | [ CRITICAL ] | Fire!") is True
    assert is_critical("00003 | [   INFO   ] | Update.") is False


def test_parse_log():
    log = "00099 | [  DEBUG  ] | Connection lost."
    level, message = parse_log(log)
    assert level == "DEBUG"
    assert message == "Connection lost."


if __name__ == "__main__":
    pytest.main([__file__])
