from typing import Optional
from datetime import datetime, timedelta

from redis.asyncio.client import Redis


async def add_mute_flag(
    redis: Redis,
    user_id: int,
    chat_id: int,
    until_date: Optional[datetime] 
) -> None:
    if not until_date:
        return

    user: str = f"user:{user_id}:{chat_id}:mute_flag"
    time_mute: int = int((until_date - datetime.now()).total_seconds())

    await redis.hset(
        name=user, 
        key='mute_flag', 
        value='True'
    )

    await redis.hexpire(
        name=user,
        seconds=time_mute,
        fields='mute_flag' 
    )


async def drop_mute_flag(
    redis: Redis,
    user_id: int,
    chat_id: int
) -> None:
    user: str = f"user:{user_id}:{chat_id}:mute_flag"

    await redis.hdel(
        'mute_flag',
        name=user
    )


async def get_mute_flag(
    redis: Redis,
    user_id: int,
    chat_id: int
) -> Optional[datetime]:
    user: str = f"user:{user_id}:{chat_id}:mute_flag"

    ttl_seconds: int = await redis.httl(
        fields='mute_flag',
        key=user
    )

    if ttl_seconds <= 0:
        return None

    time: datetime = datetime.now() + timedelta(seconds=ttl_seconds)

    return time