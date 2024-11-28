import functools
import time
from typing import Any, Callable, TypeVar

from django.db import OperationalError, connections

T = TypeVar("T")


def with_retry(
    max_retries: int = 3,
    initial_backoff: float = 1.0,
    backoff_multiplier: float = 2.0,
    exceptions: tuple = (OperationalError,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator that implements retry logic with exponential backoff for database operations.

    Args:
        max_retries: Maximum number of retry attempts
        initial_backoff: Initial backoff time in seconds
        backoff_multiplier: Multiplier for exponential backoff
        exceptions: Tuple of exceptions to catch and retry
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            retry_count = 0
            current_backoff = initial_backoff

            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retry_count += 1
                    if retry_count >= max_retries:
                        print(f"Failed after {max_retries} retries: {str(e)}")
                        raise

                    print(
                        f"Operation failed, retrying ({retry_count}/{max_retries}) after {current_backoff:.1f}s..."
                    )
                    connections.close_all()
                    time.sleep(current_backoff)
                    current_backoff *= backoff_multiplier

        return wrapper

    return decorator
