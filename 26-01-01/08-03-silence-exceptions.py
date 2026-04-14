import pytest
from contextlib import contextmanager

"""
Use @contextmanager to create a manager that "silences" specific exception types.

Requirements:
- `with silence(exc_type): ...` should catch specified exception.
- If the specified exception occurs, the code should continue without crashing (suppression).
"""

@contextmanager
def silence(exc_type):
    raise NotImplementedError()


# --- DO NOT MODIFY THE TESTS BELOW ---

def test_silence_key_error():
    d = {}
    with silence(KeyError):
        _ = d["missing_key"]
    assert True # If we reach here, it worked

def test_silence_does_not_catch_others():
    with pytest.raises(ZeroDivisionError):
        with silence(KeyError):
            _ = 1 / 0

def test_silence_flow():
    logs = []
    with silence(ValueError):
        logs.append("start")
        int("abc")
        logs.append("end") # This should not run
    
    assert logs == ["start"]

if __name__ == "__main__":
    pytest.main([__file__])
