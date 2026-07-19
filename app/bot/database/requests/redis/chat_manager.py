from typing import Optional, List

from app.bot.config import Locale
from redis.asyncio.client import Redis


async def add_chat_info(
    redis: Redis,
    chat_id: int,
    new_rules_id: Optional[int] = None,
    new_chat_locale: Optional[str] = None
) -> None:
    chat_manager: str = f"chat:{chat_id}:manager"

    check: List[Optional[str]] = await redis.hmget(
        name=chat_manager,
        keys=[
            "rules_id",
            "chat_locale"   
        ]
    )

    common_language = Locale.ENGLISH.value
    old_chat_locale: Optional[str] = check[1]
    old_rules_id: Optional[str] = check[0]

    if new_chat_locale is not None:
        chat_locale = new_chat_locale

    elif old_chat_locale is not None:
        chat_locale = old_chat_locale

    else:
        chat_locale = common_language

    if new_rules_id is not None:
        rules_id = new_rules_id

    elif old_rules_id is not None:
        rules_id = int(old_rules_id)

    else:
        rules_id = 0

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

    if rules_id is None:
        return 0

    return int(rules_id)


async def get_chat_locale(
    redis: Redis,
    chat_id: int
) -> Optional[str]:
    chat_manager: str = f"chat:{chat_id}:manager"
    common_language = Locale.ENGLISH.value

    chat_locale: Optional[str] = await redis.hget(
        name=chat_manager,
        key="chat_locale"
    )

    if chat_locale is None:
        return common_language
    
    return chat_locale