from uuid import uuid4
from typing import Union, Any, Callable, Optional
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a Cache is called
        using Redis INCR command to track the count.
    Use the qualified name of `method` using the
        `__qualname__` dunder method.
    Args:
        method: The method to be decorated

    Returns:
        Callable: The wrapped method that increments
            the counter before execution
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self) -> None:
        """Initialize Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using a random key and return the key.

        Args:
            data: The data to store. Can be a string, bytes, integer or float.

        Returns:
            str: The randomly generated key used to store the data.
        """
        key = str(uuid4())

        if isinstance(data, (int, float)):
            data = str(data).encode('utf-8')
        elif isinstance(data, str):
            data = data.encode('utf-8')

        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """
        Retrieve data from Redis by key and optionally
            convert it using the provided function.

        Args:
            key: The key to retrieve data for
            fn: Optional callable to convert the retrieved data

        Returns:
            The retrieved data, converted if a function was provided,
                or None if key doesn't exist
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn is not None else value

    def get_str(self, key: str) -> str:
        """
        Retrieve a string value from Redis by key.

        Args:
            key: The key to retrieve data for

        Returns:
            str: The retrieved string,
                or None if key doesn't exist
        """
        value = self.get(key, fn=lambda d: d.decode('utf-8'))
        return value

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer value from Redis by key.

        Args:
            key: The key to retrieve data for

        Returns:
            int: The retrieved integer,
                or None if key doesn't exist
        """
        value = self.get(key, fn=lambda d: int(d.decode('utf-8')))
        return value
