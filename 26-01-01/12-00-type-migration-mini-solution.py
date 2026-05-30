import pytest


def word_count(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def flatten(nested: list[list[int]]) -> list[int]:
    return [item for sublist in nested for item in sublist]


def test_word_count_basic() -> None:
    result = word_count("hello world hello")
    assert result == {"hello": 2, "world": 1}


def test_word_count_empty() -> None:
    assert word_count("") == {}


def test_flatten() -> None:
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]


def test_flatten_empty() -> None:
    assert flatten([]) == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
