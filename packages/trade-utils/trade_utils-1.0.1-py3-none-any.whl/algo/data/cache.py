import json
import logging
import time
from typing import Callable, List, Union

import redis

from ..config import config
from ..constant import Symbol
from .common import PricePoint, PriceStream

log = logging.getLogger(__name__)

CachableDataSource = Callable[[str, Symbol], PriceStream]


class MemoryCache():
    def __init__(self) -> None:
        self._cache_data = {}

    def has(self, cache_key: str):
        return cache_key in self._cache_data

    def get(self, cache_key: str):
        return self._cache_data[cache_key]

    def set(self, cache_key: str, data):
        self._cache_data[cache_key] = data

    def has_lock(self, cache_key: str):
        return self.has(cache_key)

    def set_lock(self, cache_key: str):
        return self.set(cache_key, 1)

    def clear_lock(self, cache_key: str):
        del self._cache_data[cache_key]


memory_cache = MemoryCache()


class RedisCache:
    def __init__(self) -> None:
        self._redis_connection = None

    def _init_redis_connection(self):
        if self._redis_connection is None:
            self._redis_connection: redis.Redis = redis.Redis.from_url(
                config.redis_url)

    def has_lock(self, cache_key: str):
        """TODO: implement lock with appropriate redis tools despite of workaround"""
        self._init_redis_connection()
        return self._redis_connection.get(cache_key) is not None

    def set_lock(self, cache_key: str):
        self._init_redis_connection()
        return self._redis_connection.set(cache_key, 1) is not None

    def clear_lock(self, cache_key: str):
        self._init_redis_connection()
        return self._redis_connection.delete(cache_key)

    def has(self, cache_key: str):
        self._init_redis_connection()
        return self._redis_connection.get(cache_key) is not None

    def get(self, cache_key: str):
        """
        may be generator. Usage uf ujson may improve performance as this class essenstially does unjsoning
        """
        self._init_redis_connection()
        data = self._redis_connection.get(cache_key)
        all_data = []

        for data_portion in json.loads(data):
            all_data.append(PricePoint.from_json_ready(data_portion))

        return all_data

    def set(self, cache_key: str, data: List[PricePoint]):
        self._init_redis_connection()
        json_ready_data = []
        for data_portion in data:
            json_ready_data.append(data_portion.to_json_ready())
        serialized_data = json.dumps(json_ready_data)
        self._redis_connection.set(cache_key, serialized_data)


redis_cache = RedisCache()


def lock_key(cache_key: str) -> str:
    """lock key format"""
    return f'{cache_key}-lock'


def cached_factory(cache_instance: Union[MemoryCache, RedisCache]):
    def _cached(cache_key: str, data_source: CachableDataSource) -> PriceStream:
        log.info('starting cached')
        lock_key_name = lock_key(cache_key)
        if cache_instance.has_lock(lock_key_name):
            log.info('found lock, waiting for data')
            while cache_instance.has_lock(lock_key_name):
                log.info('lock exists waiting')
                time.sleep(0.1)

        if cache_instance.has(cache_key):
            yield from cache_instance.get(cache_key)
        else:
            log.info('no cache reading data')
            cache_instance.set_lock(lock_key_name)
            # no cache
            # here need to arrange case for the multiprocess concurrency see README :synccache:
            all_data = []
            for data_portion in data_source:
                all_data.append(data_portion)
                yield data_portion
            cache_instance.set(cache_key, all_data)
            cache_instance.clear_lock(lock_key_name)
    return _cached


cached = cached_factory(RedisCache())
