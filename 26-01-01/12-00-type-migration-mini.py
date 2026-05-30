from typing import Dict, List

import pytest

# Fix all type issues that type checker will describe.


def word_count(text: str) -> Dict[str, int]:
    counts: Dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def flatten(nested: List[List[int]]) -> List[int]:
    return [item for sublist in nested for item in sublist]


def test_word_count_basic():
    result = word_count("hello world hello")
    assert result == {"hello": 2, "world": 1}


def test_word_count_empty():
    assert word_count("") == {}


def test_flatten():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_empty():
    assert flatten([]) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
