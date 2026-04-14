"""
Lazy Loading
- Implement a Proxy pattern where an expensive object is only initialized the first time a method is actually called.
- Key Concepts: __getattr__, Composition over Inheritance, and Lazy Initialization.
"""

import pytest


class HeavyResource:
    def __init__(self):
        self.data = "Loaded Data"
        self.initialized = True

    def query(self):
        return self.data


class LazyProxy:
    """
    Wraps a class. Does not instantiate the class until
    an attribute or method is accessed.
    """

    def __init__(self, cls, *args, **kwargs):
        self._cls = cls
        self._args = args
        self._kwargs = kwargs
        self._instance = None

    def _initialize(self):
        if self._instance is not None:
            return

        self._instance = self._cls(*self._args, **self._kwargs)

    def __getattr__(self, name):
        self._initialize()
        return getattr(self._instance, name)

    def __len__(self):
        self._initialize()
        return self._instance.__len__()


# --- DO NOT MODIFY THE TESTS BELOW ---


def test_lazy_initialization_timing():
    proxy = LazyProxy(HeavyResource)
    assert proxy._instance is None
    assert proxy.query() == "Loaded Data"
    assert proxy._instance is not None


def test_attribute_delegation():
    proxy = LazyProxy(HeavyResource)
    assert proxy.initialized is True


def test_method_calling():
    proxy = LazyProxy(list, [1, 2, 3])
    proxy.append(4)
    assert len(proxy) == 4


def test_multiple_proxies_independence():
    p1 = LazyProxy(list)
    p2 = LazyProxy(list)
    p1.append(1)
    assert len(p1) == 1
    assert len(p2) == 0


def test_getattr_raises_correct_error():
    proxy = LazyProxy(HeavyResource)
    with pytest.raises(AttributeError):
        _ = proxy.non_existent_field


if __name__ == "__main__":
    pytest.main([__file__])
