from typing import Optional

from database.redis import async_redis


async def get_old_message(
    user_id: int, 
    message: str
    ) -> Optional[str]:
    user: str = f"user:{user_id}:unique_messages"

    async with async_redis as redis:
        old_message = await redis.getset(name=user, value=message)
        await redis.expire(name=user, time=12)

        if old_message:
            return old_message
        return None


async def get_count_messages(
    user_id: int, 
    message: str
    ) -> int:
    user: str = f"user:{user_id}:repeated_messages"

    async with async_redis as redis:
        await redis.rpush(user, message)
        await redis.expire(name=user, time=12)

        count: int = await redis.llen(user)
        return count