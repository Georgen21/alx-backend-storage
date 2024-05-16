#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests
from functools import wraps
from typing import Callable

redis_client = redis.Redis()

def cache_with_expiration(expiration: int):
    """
    Decorator to cache the result of a function in Redis with an expiration time.

    Args:
        expiration (int): The expiration time in seconds.

    Returns:
        Callable: The decorator function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            cache_key = f"cache:{url}"
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            result = func(url)
            redis_client.setex(cache_key, expiration, result)
            return result
        return wrapper
    return decorator

def count_calls(func: Callable) -> Callable:
    """
    Decorator to count how many times a particular URL is accessed.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with call counting.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        redis_client.incr(count_key)
        return func(url)
    return wrapper

@cache_with_expiration(10)
@count_calls
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL and return it.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(test_url))
    print(get_page(test_url))
    count_key = f"count:{test_url}"
    print(f"URL {test_url} was accessed {redis_client.get(count_key).decode('utf-8')} times.")
