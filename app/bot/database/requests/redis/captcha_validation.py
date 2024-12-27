from typing import Optional
from datetime import datetime, timedelta

from app.bot.database.redis import async_redis


async def add_mute_flag(
    user_id: int,
    chat_id: int,
    until_date: Optional[datetime] 
) -> None:
    if not until_date:
        return

    user: str = f"user:{user_id}:{chat_id}:mute_flag"
    time_mute: int = int((until_date - datetime.now()).total_seconds())

    async with async_redis as redis:
        await redis.hset(
            name=user, 
            key='mute_flag', 
            value=True
        )

        await redis.hexpire(
            'mute_flag', 
            time_mute, 
            name=user
        )


async def drop_mute_flag(
    user_id: int,
    chat_id: int
) -> None:
    user: str = f"user:{user_id}:{chat_id}:mute_flag"

    async with async_redis as redis:
        get_flag: bool = await redis.hexists(
            name='mute_flag',
            key=user
        )

        if get_flag:
            await redis.hdel(
                name='mute_flag',
                key=user
            )


async def get_mute_flag(
    user_id: int,
    chat_id: int
) -> Optional[datetime]:
    user: str = f"user:{user_id}:{chat_id}:mute_flag"

    async with async_redis as redis:
        get_flag: bool = await redis.hexists(
            name='mute_flag',
            key=user
        )

        if get_flag:
            ttl_seconds: int = await redis.httl(
                'mute_flag',
                key=user
            )

            time: datetime = datetime.now() + timedelta(seconds=ttl_seconds)

            return time
        return None