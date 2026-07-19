from typing import Callable, Dict, Any, Awaitable, Optional
from datetime import timedelta, datetime

from redis.asyncio.client import Redis
from aiogram_i18n import I18nContext
from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    MessageReactionUpdated, 
    TelegramObject, Update
)

from app.bot.database import get_chat_locale
from app.bot.utils import count_reactions_spam


class ReactionsAntiSpamMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, bot: Bot):
        self.until_date: datetime = datetime.now() + timedelta(minutes=30)
        self.redis: Redis = redis
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.message_reaction:
            reaction: MessageReactionUpdated = event.message_reaction
            i18n: Optional[I18nContext] = data.get('i18n')
            locale: Optional[str] = get_chat_locale(
                chat_id=reaction.chat.id,
                redis=self.redis
            )

            if not i18n:
                return await handler(event, data)

            if reaction.new_reaction:
                await count_reactions_spam(
                    redis=self.redis,
                    bot=self.bot,
                    locale=locale,
                    i18n=i18n,
                    until_date=self.until_date,
                    reactions=reaction,
                    count_spam=3
                )

            return await handler(event, data)
        return await handler(event, data)