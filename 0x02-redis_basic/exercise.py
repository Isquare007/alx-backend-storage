#!/usr/bin/env python3
"""Exercise"""
from typing import Union
import redis
import uuid


class Cache:
    """Store an instance of redis client"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key