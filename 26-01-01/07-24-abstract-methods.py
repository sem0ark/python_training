"""
Enforcing the Plugin Interface (ABC)
Create an abstract base class "DataProcessor" that forces all plugins to implement a "process" method.
"""

from abc import ABC, abstractmethod

import pytest


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data):
        pass


class UppercaseProcessor(DataProcessor):
    """Implement the abstract method to return data in uppercase"""


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_abstract_enforcement():
    # This should fail because process() is not implemented
    class IncompleteProcessor(DataProcessor):
        pass

    with pytest.raises(TypeError):
        IncompleteProcessor()


def test_processor_logic():
    proc = UppercaseProcessor()
    assert proc.process("hello") == "HELLO"


def test_abc_instantiation_fails():
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        DataProcessor()


def test_processor_logic():
    assert UppercaseProcessor().process("hello") == "HELLO"


def test_processor_with_numbers():
    assert UppercaseProcessor().process(123) == "123"


def test_subclass_verification():
    assert issubclass(UppercaseProcessor, DataProcessor)


def test_incomplete_subclass_fails():
    class Incomplete(DataProcessor):
        pass

    with pytest.raises(TypeError):
        Incomplete()


def test_processor_empty_string():
    assert UppercaseProcessor().process("") == ""


if __name__ == "__main__":
    pytest.main([__file__])
