#!/usr/bin/env python3
"""A module for implementing a web page caching system using Redis.
"""
import redis
import requests
from functools import wraps
from typing import Callable


def count_calls(method: Callable) -> Callable:
    """Decorator to track the number of calls to a URL.
    """
    @wraps(method)
    def wrapper(url):
        """Wrapper function that maintains the count.
        """
        client = redis.Redis()
        client.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_page(method: Callable) -> Callable:
    """Decorator to cache page content with expiration.
    """
    @wraps(method)
    def wrapper(url):
        """Wrapper function that implements caching.
        """
        client = redis.Redis()
        cached = client.get(f"cached:{url}")
        if cached:
            return cached.decode('utf-8')
        result = method(url)
        client.setex(f"cached:{url}", 10, result)
        return result
    return wrapper


@count_calls
@cache_page
def get_page(url: str) -> str:
    """Fetches a page and caches the result with expiration.

    Args:
        url (str): The URL to fetch

    Returns:
        str: The content of the URL
    """
    return requests.get(url).text
