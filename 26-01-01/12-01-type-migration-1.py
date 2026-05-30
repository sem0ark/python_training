from typing import Any, List, Optional

import pytest

"""
Goal: Debug and refine an infrastructure monitoring module to ensure type safety 
and logical correctness when handling node telemetry.

Requirements:
1. The `process_fleet_telemetry` function must accept a list of specialized `ComputeNode` objects. The type hint must support covariance to allow subtypes of `Node` in the collection.
2. The `fetch_node_metadata` function must treat `0` as a valid node identifier. It currently incorrectly filters out ID 0 due to truthiness checks.
3. Replace the `Any` return type in `get_system_manifest` with a structured definition. The returned data must contain `version` (int) and `tags` (list of strings).
4. Ensure that the `audit_config` function can access the structured data from the manifest without relying on dynamic `Any` lookups.

Scenario: The monitoring system for "Existential Computing Ltd." is failing to track its most important node (ID 0) and refuses to recognize specialized compute hardware as valid nodes.
"""


class Node:
    def __init__(self, name: str):
        self.name = name


class ComputeNode(Node):
    def __init__(self, name: str, cores: int):
        super().__init__(name)
        self.cores = cores


# --- BUGGY IMPLEMENTATION ---


def process_fleet_telemetry(nodes: List[Node]) -> List[str]:
    """Return a list of node names processed."""
    return [n.name for n in nodes]


def fetch_node_metadata(node_id: Optional[int]) -> str:
    """
    Fetch metadata for a node.
    Node ID 0 is the 'Master Gateway' and must be supported.
    """
    if not node_id:
        return "Unknown Node"

    return f"Metadata for Node {node_id}"


def get_system_manifest() -> Any:
    """
    Returns the system configuration.
    (The third-party API returns this as a raw dictionary, but we need structure.)
    """
    return {"version": 2, "tags": ["production", "edge", "legacy"]}


def audit_config() -> bool:
    """Verifies the manifest contains required fields."""
    manifest = get_system_manifest()
    # This should be type-safe, currently relies on 'Any'
    return "version" in manifest and isinstance(manifest["version"], int)


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_process_fleet_telemetry_accepts_subtypes():
    # In a strictly typed environment (MyPy), passing list[ComputeNode]
    # to list[Node] would fail. We test the logic here.
    fleet: List[ComputeNode] = [ComputeNode("Alpha", 8), ComputeNode("Beta", 16)]
    try:
        results = process_fleet_telemetry(fleet)
        assert len(results) == 2
        assert "Alpha" in results
    except TypeError as e:
        pytest.fail(f"Type variance issue: {e}")


def test_fetch_node_metadata_id_zero():
    # ID 0 is a valid system ID (The Master Gateway)
    result = fetch_node_metadata(0)
    assert result == "Metadata for Node 0", (
        "Node ID 0 should be recognized as a valid ID"
    )


def test_fetch_node_metadata_none():
    assert fetch_node_metadata(None) == "Unknown Node"


def test_fetch_node_metadata_positive():
    assert fetch_node_metadata(123) == "Metadata for Node 123"


def test_manifest_structure_integrity():
    # This test ensures the manifest returns the expected keys
    manifest = get_system_manifest()
    assert "version" in manifest
    assert isinstance(manifest["tags"], list)
    assert "production" in manifest["tags"]


def test_audit_config_verification():
    assert audit_config() is True


def test_type_safety_definitions():
    # This checks if the student defined a TypedDict or similar for the manifest
    # by inspecting the return annotation of get_system_manifest
    annotations = get_system_manifest.__annotations__
    assert annotations.get("return") is not Any, (
        "get_system_manifest should not return 'Any'"
    )

    # Check if process_fleet_telemetry is using a covariant container
    telemetry_annotations = process_fleet_telemetry.__annotations__
    container_type = telemetry_annotations.get("nodes")
    # Sequence and Iterable are covariant; List is invariant.
    assert "List" not in str(container_type), (
        "Use a covariant collection type like Sequence or Iterable"
    )


if __name__ == "__main__":
    pytest.main([__file__])

# --- Hints ---
# - Task 1.1: Python's 'list' is invariant. Look into 'typing.Sequence' or 'typing.Iterable' for covariance.
# - Task 1.2: 'if not x' evaluates to True for None, but also for the integer 0. Use an explicit identity check.
# - Task 1.3: Use 'typing.TypedDict' to define the shape of the manifest dictionary.
