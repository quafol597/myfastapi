from asgiref.sync import async_to_sync
from functools import wraps
import asyncio


def task_decorator(async_func):

    @wraps(async_func)
    def inner(*args, **kwargs):
        event_loop = asyncio.get_event_loop()
        return event_loop.run_until_complete(async_func(*args, **kwargs))

    return inner
