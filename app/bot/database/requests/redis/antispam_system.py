from typing import Optional

from app.bot.database.redis import async_redis


async def get_old_message(
    user_id: int, 
    chat_id: int,
    message: str
    ) -> Optional[str]:
    user: str = f"user:{user_id}:{chat_id}:unique_messages"     

    async with async_redis as redis:
        old_message: Optional[str] = await redis.getset(name=user, value=message)
        await redis.expire(name=user, time=12)

        if old_message:
            return old_message
        return None


async def get_count_messages(   
    user_id: int, 
    chat_id: int,
    message: str
    ) -> int:
    user: str = f"user:{user_id}:{chat_id}:repeated_messages"

    async with async_redis as redis:
        await redis.rpush(user, message)
        await redis.expire(name=user, time=12)

        count_messages: int = await redis.llen(user)
        return count_messages


async def get_count_reactions(
    user_id: int, 
    chat_id: int
    ) -> int:
    user: str = f"user:{user_id}:{chat_id}:reactions"

    async with async_redis as redis:
        await redis.rpush(user, 'reaction')
        await redis.expire(name=user, time=20)

        count_reactions: int = await redis.llen(user)
        return count_reactions
