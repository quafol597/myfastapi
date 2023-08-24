from functools import wraps
import asyncio


def async_to_sync(async_func):

    @wraps(async_func)
    def inner(*args, **kwargs):
        event_loop = asyncio.get_event_loop()
        return event_loop.run_until_complete(async_func(*args, **kwargs))

    return inner
