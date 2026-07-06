import redis
from loguru import logger

from app.core.config import settings


class RedisClient:
    _instance: redis.Redis | None = None

    @classmethod
    def get_instance(cls) -> redis.Redis:
        if cls._instance is None:
            cls._instance = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                password=settings.REDIS_PASSWORD,
                decode_responses=True,
            )
            try:
                cls._instance.ping()
                logger.info("Redis connection established successfully")
            except redis.ConnectionError as e:
                logger.error(f"Failed to connect to Redis: {e}")
                raise
        return cls._instance

    @classmethod
    def set(cls, key: str, value: str, expire: int | None = None) -> None:
        client = cls.get_instance()
        if expire:
            client.set(key, value, ex=expire)
        else:
            client.set(key, value)

    @classmethod
    def get(cls, key: str) -> str | None:
        client = cls.get_instance()
        return client.get(key)

    @classmethod
    def delete(cls, key: str) -> None:
        client = cls.get_instance()
        client.delete(key)

    @classmethod
    def exists(cls, key: str) -> bool:
        client = cls.get_instance()
        return client.exists(key) > 0
