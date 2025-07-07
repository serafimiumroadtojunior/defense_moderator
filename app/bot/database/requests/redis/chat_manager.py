from typing import Optional, List

from redis.asyncio.client import Redis


async def add_chat_info(
    redis: Redis,
    chat_id: int,
    rules_id: Optional[int] = None,
    chat_locale: Optional[str] = None
) -> None:
    chat_manager: str = f"chat:{chat_id}:manager"

    check: Optional[List[str]] = await redis.hmget(
        name=chat_manager,
        keys=[
            "rules_id",
            "chat_locale"   
        ]
    )

    if not check:
        return None
    
    if not check[0] and not check[1]:
        return None

    old_chat_locale: str = check[1]
    old_rules_id = int(check[0])
    chat_locale: str = old_chat_locale if not chat_locale else chat_locale
    rules_id: int = old_rules_id if not rules_id else rules_id

    await redis.hset(
        name=chat_manager,
        mapping={
            "rules_id": rules_id,
            "chat_locale": chat_locale
        }
    )


async def get_rules_id(
    redis: Redis,
    chat_id: int
) -> Optional[int]:
    chat_manager: str = f"chat:{chat_id}:manager"

    rules_id: Optional[str] = await redis.hget(
        name=chat_manager,
        key="rules_id"
    )

    if not rules_id:
        return None

    return int(rules_id)
    


async def get_chat_locale(
    redis: Redis,
    chat_id: int
) -> Optional[str]:
    chat_manager: str = f"chat:{chat_id}:manager"

    chat_locale: Optional[str] = await redis.hget(
        name=chat_manager,
        key="chat_locale"
    )

    if not chat_locale:
        return None
    
    return chat_locale