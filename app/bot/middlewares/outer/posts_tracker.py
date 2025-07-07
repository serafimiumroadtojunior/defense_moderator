from typing import Any, Awaitable, Callable, Dict, Optional

from redis.asyncio.client import Redis
from aiogram import BaseMiddleware
from aiogram_i18n import I18nContext
from aiogram.types import TelegramObject, Message, Chat

from app.bot.database import get_rules_id, get_chat_locale


class ChannelPostMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.is_automatic_forward:
            chat: Chat = event.chat
            i18n: Optional[I18nContext] = data.get('i18n')
            rules_message_id: Optional[int] = await get_rules_id(
                chat_id=chat.id,
                redis=self.redis
            )

            if not chat.type == 'channel':
                return await handler(event, data)
            
            if not i18n:
                return await handler(event, data)

            if rules_message_id:
                locale: Optional[str] = await get_chat_locale(
                    chat_id=chat.id,
                    redis=self.redis
                )

                await event.reply(
                    text=i18n.get(
                        "new-post",
                        locale,
                        chat_id=chat.id,
                        rules_id=rules_message_id
                    )
                )
                return await handler(event, data)

            return await handler(event, data)
        return await handler(event, data)