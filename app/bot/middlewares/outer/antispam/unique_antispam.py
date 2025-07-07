from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Dict, Optional

from redis.asyncio.client import Redis
from aiogram_i18n import I18nContext
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject
from spacy import load
from spacy.language import Language

from app.bot.database import get_chat_locale
from app.bot.utils import unique_messages_spam, unique_words_spam


class UniqueAntiSpamMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, bot: Bot):
        self.redis: Redis = redis
        self.bot: Bot = bot
        self.until_date: datetime = datetime.now() + timedelta(minutes=30)
        self.nlp: Language = load("ru_core_news_sm")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            i18n: Optional[I18nContext] = data.get('i18n')
            locale: Optional[str] = get_chat_locale(
                chat_id=event.chat.id,
                redis=self.redis
            )

            if not i18n:
                return await handler(event, data)

            await unique_messages_spam(
                bot=self.bot,
                redis=self.redis,
                locale=locale,
                i18n=i18n,
                message=event,
                nlp_model=self.nlp,
                until_date=self.until_date
            )

            await unique_words_spam(
                bot=self.bot,
                redis=self.redis,
                locale=locale,
                i18n=i18n,
                message=event,
                nlp_model=self.nlp,
                until_date=self.until_date,
                count_spam=3
            )

            return await handler(event, data)
        return handler(event, data)