#!/usr/bin/env python3
"""Exercise"""
from typing import Union, Callable, Optional
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)

        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)

        return output

    return wrapper


def replay(fn: Callable):
    r = redis.Redis()
    f_name = fn.__qualname__
    n_calls = r.get(f_name)
    try:
        n_calls = n_calls.decode('utf-8')
    except Exception:
        n_calls = 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ""

        print(f'{f_name}(*{i}) -> {o}')


class Cache:
    """Store an instance of redis client"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
