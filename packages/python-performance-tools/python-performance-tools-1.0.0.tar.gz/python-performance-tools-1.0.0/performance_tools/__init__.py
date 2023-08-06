import sys

from typing import Callable
from time import perf_counter
from contextlib import contextmanager


@contextmanager
def catch_time(message: str = None, condition_function: Callable = None) -> float:
    """Usage example:
    """
    if condition_function:
        if condition_function():
            start = perf_counter()
            yield lambda: perf_counter() - start

            print(f"Time: {perf_counter() - start} :: {message}", file=sys.stderr)
        else:
            yield
    else:

        start = perf_counter()
        yield lambda: perf_counter() - start

        print(f"Time: {perf_counter() - start} :: {message}", file=sys.stderr)

__all__ = ("catch_time", )
