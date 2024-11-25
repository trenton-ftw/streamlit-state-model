from typing import Callable, TypeVar

T = TypeVar("T") 

class DefaultFactory:
    """
    Wrapper class to specify a default factory for an attribute.
    """

    default_factory: Callable[[], T]
    "The actual callable that will return the default value."

    def __init__(self, default_factory: Callable[[], T]):
        self.default_factory = default_factory
