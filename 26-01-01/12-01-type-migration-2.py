import inspect
from typing import Any, Callable, Self

import pytest

"""
Goal: Refactor the "Entropy Analytics" data pipeline to use modern Python 3.12+ generics and preserve type metadata across decorators.

Requirements:
1. Consolidate the `get_first_metric` and `get_first_log` functions into a single generic function named `extract_first`. Use PEP 695 square-bracket syntax for the type parameter.
2. Implement a generic `DataEnvelope` class using PEP 695 syntax. The class must store a `content` attribute of a generic type and a `timestamp` (float).
3. Update the `BasePayload` hierarchy so that `validate_and_return` accepts any subtype of `BasePayload` and returns that same subtype (not the base).
4. Modernize the `ProcessingNode` class to use the `Self` type for its `clone` and `link_to` methods.
5. Fix the `audit_trace` decorator. It must preserve the original function's signature, name, and docstring. It must also correctly hint that it returns the same type as the wrapped function.

Scenario: Entropy Analytics (where data goes to become slightly more disorganized) is suffering from "type rot." The IDE can no longer track objects through the pipeline, and the senior architect has banned the word "Any" from the codebase.
"""

# --- LEGACY IMPLEMENTATION TO REFACTOR ---


class BasePayload:
    def verify(self) -> bool:
        return True


class MetricPayload(BasePayload):
    def __init__(self, value: float):
        self.value = value


class LogPayload(BasePayload):
    def __init__(self, message: str):
        self.message = message


# TODO: Replace these with a single generic 'extract_first'
def get_first_metric(items: list[MetricPayload]) -> MetricPayload:
    return items[0]


def get_first_log(items: list[LogPayload]) -> LogPayload:
    return items[0]


# TODO: Refactor to use PEP 695 generic syntax
class DataEnvelope:
    def __init__(self, content: Any, timestamp: float):
        self.content = content
        self.timestamp = timestamp


# TODO: Use a bounded generic to ensure the return type matches the input subtype
def validate_and_return(payload: BasePayload) -> BasePayload:
    if payload.verify():
        return payload
    raise ValueError("Invalid payload")


class ProcessingNode:
    def __init__(self, name: str):
        self.name = name
        self.next_node: "ProcessingNode" | None = None

    # TODO: Use modern self-referential type hinting
    def link_to(self, other: "ProcessingNode") -> "ProcessingNode":
        self.next_node = other
        return other

    def clone(self) -> "ProcessingNode":
        return ProcessingNode(f"{self.name}_copy")


# TODO: Fix metadata loss and improve type hinting using ParamSpec
def audit_trace(func: Callable):
    def wrapper(*args, **kwargs):
        print(f"Tracing {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


@audit_trace
def transform_data(factor: int, label: str) -> str:
    """Multiplies label by factor."""
    return label * factor


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_generic_extractor():
    metrics = [MetricPayload(1.1), MetricPayload(2.2)]
    logs = [LogPayload("start"), LogPayload("end")]

    from __main__ import extract_first

    assert extract_first(metrics).value == 1.1
    assert extract_first(logs).message == "start"
    assert hasattr(extract_first, "__type_params__"), "Must use PEP 695 [T] syntax"


def test_generic_envelope_typing():
    from __main__ import DataEnvelope

    env = DataEnvelope(MetricPayload(42.0), 1600000000.0)
    assert env.content.value == 42.0
    assert hasattr(DataEnvelope, "__type_params__"), (
        "DataEnvelope must use PEP 695 [T] syntax"
    )


def test_bounded_generic_payload():
    metric = MetricPayload(5.5)
    result = validate_and_return(metric)
    assert isinstance(result, MetricPayload)

    sig = inspect.signature(validate_and_return)
    param_type = sig.parameters["payload"].annotation
    assert param_type != BasePayload, (
        "Should use a TypeVar/Generic bounded to BasePayload"
    )


def test_self_referential_modernization():
    node_a = ProcessingNode("A")
    node_b = ProcessingNode("B")
    linked = node_a.link_to(node_b)

    assert linked is node_b
    assert node_a.clone().name == "A_copy"

    hints = ProcessingNode.clone.__annotations__
    assert hints.get("return") is Self, "clone() should return 'Self'"


def test_decorator_metadata_preservation():
    assert transform_data.__name__ == "transform_data"
    assert transform_data.__doc__ == "Multiplies label by factor."

    sig = inspect.signature(transform_data)
    assert "factor" in sig.parameters
    assert sig.parameters["factor"].annotation is int
    assert sig.return_annotation is str


def test_decorator_paramspec_implementation():
    assert hasattr(transform_data, "__wrapped__"), "Decorator must use @wraps"


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - PEP 695 (Python 3.12): Use 'def func[T](arg: T) -> T:' instead of TypeVar.
# - Bounded Generics: Use 'def func[T: BaseClass](arg: T) -> T:'.
# - Decorators: Use 'typing.ParamSpec' (P) and 'typing.TypeVar' (R) to define 'Callable[P, R]' for the input and return types.
# - Self-reference: The 'typing.Self' type (introduced in 3.11) replaces string literals like '"ClassName"'.
