from redis.asyncio.client import Redis


async def get_report_flag(
    redis: Redis,
    user_id: int, 
    chat_id: int
) -> bool:
    user: str = f"user:{user_id}:{chat_id}:report"

    report_flag: bool = await redis.hexists(
        name=user,
        key='report_flag'
    )

    return report_flag


async def add_report_flag(
    redis: Redis,
    user_id: int, 
    chat_id: int
) -> bool:
    user: str = f"user:{user_id}:{chat_id}:report"

    flag: bool = await get_report_flag(
        redis=redis,
        user_id=user_id,
        chat_id=chat_id
    )

    if not flag:
        await redis.hset(
            name=user,
            key='report_flag',
            value='True'
        )

        await redis.hexpire(
            name=user,
            fields='report_flag',
            seconds=3600
        )

        return True
    return False