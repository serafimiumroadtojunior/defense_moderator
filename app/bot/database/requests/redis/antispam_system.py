from typing import Optional, Dict

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
    chat_id: int,
    emoji: str
) -> int:
    user: str = f"user:{user_id}:{chat_id}:reactions"

    async with async_redis as redis:
        await redis.rpush(user, emoji)
        await redis.expire(name=user, time=20)

        count_reactions: int = await redis.llen(user)
        return count_reactions


async def add_stats_messages(
    user_id: int,
    message_text: str
) -> None:
    user_stats: str = f"user:{user_id}:messages_stats"
    user_messages: str = f"user:{user_id}:messages"

    async with async_redis as redis:
        checker: bool = await redis.hexists(
            name=user_stats,
            key='stats'
        )

        if not checker:
            await redis.hset(
                name=user_stats,
                key='stats',
                mapping={
                    'all_messages' : 0,
                    'not_unique_messages' : 0,
                }
            )

        if await redis.sismember(
            name=user_messages,
            value=message_text
        ) == 0:
            await redis.sadd(
                message_text,
                name=user_messages
            )

            await redis.hincrby(
                name=user_stats,
                key='all_messages'
            )

        await redis.hincrby(
            name=user_stats,
            key='not_unique_messages'
        )


async def get_messages_percent(user_id: int) -> Optional[float]:
    user_stats: str = f"user:{user_id}:messages_stats"

    async with async_redis as redis:
        checker: bool = await redis.hexists(
            name=user_stats,
            key='stats'
        )

        if checker:
            stats: Dict[str, int] = await redis.hgetall(name=user_stats)

            if stats['all_messages'] >= 5:
                all_messages: int = stats['all_messages']
                not_unique_messages: int = stats['not_unique_messages']
                percentage: float = (not_unique_messages / all_messages) * 100

                return percentage
            return None
