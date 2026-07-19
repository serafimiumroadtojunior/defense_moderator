from typing import (
    Any, Awaitable, 
    Callable, Dict,
    Optional
)

from redis.asyncio.client import Redis
from aiogram_i18n import I18nContext
from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, Update,
    ChatMemberUpdated, User
)

from app.bot.utils import answer_message
from app.bot.database import get_chat_locale


class GoodbyeMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, bot: Bot):
        self.redis: Redis = redis
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat_member:
            i18n: Optional[I18nContext] = data.get('i18n')
            member: ChatMemberUpdated = event.chat_member
            chat_id: int = member.chat.id
            new_member = member.new_chat_member
            old_member = member.old_chat_member

            if not i18n:
                return await handler(event, data)

            if new_member.status == "left" or old_member.status == "left":
                user: User = member.from_user
                locale: Optional[str] = await get_chat_locale(
                    chat_id=chat_id,
                    redis=self.redis
                )


                await answer_message(
                    bot=self.bot,
                    chat_id=chat_id,
                    text=i18n.get(
                        'goodbye-message',
                        locale,
                        user_name=user.full_name,
                        user_id=user.id
                    )   
                )

            return await handler(event, data)
        return await handler(event, data)