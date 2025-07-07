from typing import Any, Awaitable, Callable, Dict, Optional

from redis.asyncio.client import Redis
from aiogram import BaseMiddleware, Bot
from aiogram_i18n import I18nContext
from aiogram.types import Update, TelegramObject

from app.bot.database import get_chat_locale
from app.bot.utils import parse_messages_percent


class PercentSpamParseMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, bot: Bot):
        self.redis: Redis = redis
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.message:
            i18n: Optional[I18nContext] = data.get('i18n')
            locale: Optional[str] = get_chat_locale(
                chat_id=event.message.chat.id,
                redis=self.redis
            )

            if not i18n:
                return await handler(event, data)

            if event.chat_member:
                await parse_messages_percent(
                    bot=self.bot,
                    locale=locale,
                    i18n=i18n,
                    member=event.chat_member
                )
                return await handler(event, data)
            
            return await handler(event, data)
        return await handler(event, data)