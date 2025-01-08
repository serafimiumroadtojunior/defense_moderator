from app.bot.database.redis import async_redis


async def get_report_flag(
    user_id: int, 
    chat_id: int
) -> bool:
    user: str = f"user:{user_id}:{chat_id}:report"

    async with async_redis as redis:
        report_flag: bool = await redis.hexists(
            name=user,
            key='report_flag'
        )

        return report_flag


async def add_report_flag(
    user_id: int, 
    chat_id: int
) -> bool:
    user: str = f"user:{user_id}:{chat_id}:report"

    async with async_redis as redis:
        flag: bool = await get_report_flag(
            user_id=user_id,
            chat_id=chat_id
        )

        if not flag:
            await redis.hset(
                name=user,
                key='report_flag',
                value=True
            )

            await redis.hexpire(
                'report_flag',
                name=user,
                seconds=3600
            )

            return True
        return False