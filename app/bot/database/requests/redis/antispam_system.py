from typing import Optional

from redis.asyncio.client import Redis


async def get_old_message(
    redis: Redis,
    user_id: int, 
    chat_id: int,
    message: str
) -> Optional[str]:
    user: str = f"user:{user_id}:{chat_id}:unique_messages"     

    old_message: Optional[str] = await redis.getset(
        name=user, 
        value=message
    )

    await redis.expire(
        name=user, 
        time=12
    )

    if old_message:
        return old_message

    return None


async def get_count_messages( 
    redis: Redis,  
    user_id: int, 
    chat_id: int,
    message: str
) -> int:
    user: str = f"user:{user_id}:{chat_id}:repeated_messages"

    await redis.rpush(user, message)
    await redis.expire(
        name=user, 
        time=12
    )

    count_messages: int = await redis.llen(
        name=user
    )

    return count_messages


async def get_count_reactions(
    redis: Redis,
    user_id: int, 
    chat_id: int,
    emoji: str
) -> int:
    user: str = f"user:{user_id}:{chat_id}:reactions"

    await redis.rpush(user, emoji) 
    await redis.expire(
        name=user, 
        time=20
    ) 

    count_reactions: int = await redis.llen(
        name=user
    )
 
    return count_reactions


async def message_counter(
    redis: Redis,
    user_id: int,
    message_text: str
) -> int:
    user_messages: str = f"user:{user_id}:messages"

    await redis.sadd(
        values=message_text, 
        name=user_messages
    )

    count_unique: int = await redis.scard(
        name=user_messages
    )

    return count_unique