from typing import Optional, List

from app.bot.database.redis import async_redis


async def add_chat_info(
    chat_id: int,
    rules_id: Optional[int] = None,
    chat_locale: str = "en"
) -> None:
    chat_manager: str = f"chat:{chat_id}:manager"

    async with async_redis as redis:
        check: List[Optional[str]] = await redis.hmget(
            name=chat_manager,
            keys=[
                "rules_id",
                "chat_locale"   
            ]
        )

        old_rules_id: Optional[int] = int(check[0])
        if not old_rules_id:
            return None

        rules_id: int = old_rules_id if not rules_id else rules_id

        await redis.hset(
            name=chat_manager,
            mapping={
                "rules_id": rules_id,
                "chat_locale": chat_locale
            }
        )


async def get_rules_id(
    chat_id: int
) -> Optional[int]:
    chat_manager: str = f"chat:{chat_id}:manager"

    async with async_redis as redis:
        rules_id: Optional[str] = await redis.hget(
            name=chat_manager,
            key="rules_id"
        )

        if not rules_id:
            return None

        return int(rules_id)
    


async def get_chat_locale(
    chat_id: int
) -> str:
    chat_manager: str = f"chat:{chat_id}:manager"

    async with async_redis as redis:
        chat_locale: Optional[str] = await redis.hget(
            name=chat_manager,
            key="chat_locale"
        )

        if not chat_locale:
            return 'en'
        
        return chat_locale