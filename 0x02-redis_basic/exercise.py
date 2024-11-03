#!/usr/bin/env python3
"""
Module for Redis-based NoSQL Database."""
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


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs
        and outputs for a function using
        Redis lists to store the history.

    Args:
        method: The method to be decorated

    Return:
        Callable: The wrapped method that stores
            input/output history
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function

    Args:
        method: The method to display history for
    """
    if method is None or not hasattr(method, '__self__'):
        return

    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    mthd_name = method.__qualname__
    in_key = '{}:inputs'.format(mthd_name)
    out_key = '{}:outputs'.format(mthd_name)
    fxn_call_count = 0
    if redis_store.exists(mthd_name) != 0:
        fxn_call_count = int(redis_store.get(mthd_name))
    print('{} was called {} times:'.format(mthd_name, fxn_call_count))
    mthd_inputs = redis_store.lrange(in_key, 0, -1)
    mthd_outputs = redis_store.lrange(out_key, 0, -1)
    for mthd_inputs, mthd_output in zip(mthd_inputs, mthd_outputs):
        print('{}(*{}) -> {}'.format(
            mthd_name,
            mthd_inputs.decode("utf-8"),
            mthd_output,
        ))


class Cache:
    """
    A class to store and retrieve data using Redis.
    """
    def __init__(self) -> None:
        """Initialize Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
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
