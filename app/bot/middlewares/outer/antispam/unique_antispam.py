from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Dict, Optional

from fluentogram import TranslatorRunner
from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject
from spacy import load
from spacy.language import Language

from app.bot.utils import unique_messages_spam, unique_words_spam


class UniqueAntiSpamMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.until_date: datetime = datetime.now() + timedelta(minutes=30)
        self.nlp: Language = load("ru_core_news_sm")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            bot: Optional[Bot] = data.get('bot')
            i18n: Optional[TranslatorRunner] = data.get('i18n')

            if not bot or not i18n:
                return await handler(event, data)

            await unique_messages_spam(
                bot=bot,
                i18n=i18n,
                message=event,
                nlp_model=self.nlp,
                until_date=self.until_date
            )

            await unique_words_spam(
                bot=bot,
                i18n=i18n,
                message=event,
                nlp_model=self.nlp,
                until_date=self.until_date,
                count_spam=3
            )

        return handler(event, data)