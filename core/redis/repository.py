from aioredis import Redis


class RedisRepository:
    def __init__(self, redis: Redis):
        self._redis = redis

    async def set(self, key: str, value: str, expire: int = 0):
        return await self._redis.set(key, value, ex=expire)

    async def get(self, key: str):
        return await self._redis.get(key)
