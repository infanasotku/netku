from typing import Callable


def retry(func: Callable, times: int = 5):
    """Decorates callable with retrying it `times` times.

    - Note Retries work only for python `Exception`.
    """

    async def repeat_request(*args, **kwargs):
        times_left = times
        while True:
            try:
                times_left -= 1
                return await func(*args, **kwargs)
            except Exception:
                if not times_left:
                    raise

    return repeat_request
