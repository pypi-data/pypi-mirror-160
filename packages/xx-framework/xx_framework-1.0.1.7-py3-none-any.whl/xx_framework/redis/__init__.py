import redis
from xx_framework.conf import config

redis_config = config.REDIS


class MyRedisPool:
    def __new__(cls, *args, **kwargs) -> object:
        if not hasattr(cls, '_instance'):
            setattr(cls, '_instance', super(__class__, cls).__new__(cls, *args, **kwargs))
        return getattr(cls, '_instance')

    def __init__(self):
        self._conn_pool = redis.ConnectionPool(**config.REDIS)

    def pool(self):
        return self._conn_pool

    def redis(self):
        return redis.Redis(connection_pool=self.pool())


my_redis_pool = MyRedisPool()

__ALL__ = [
    my_redis_pool
]
