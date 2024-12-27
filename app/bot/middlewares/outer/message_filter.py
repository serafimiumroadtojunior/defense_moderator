from datetime import datetime, timedelta
from typing import Any, Awaitable, Callable, Dict, List

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject
from spacy import load
from spacy.language import Language

from app.bot.utils import check_message_to_bad_words, check_message_to_https_links


class FilterWordsMiddleware(BaseMiddleware):
    def __init__(
        self,
        bot: Bot,
        file_path: str
    ):
        self.bot = bot
        self.forbidden_words_file = file_path
        self.forbidden_words: List[str] = self.load_forbidden_words()
        self.until_date: datetime = datetime.now() + timedelta(minutes=30)
        self.nlp: Language = load("ru_core_news_sm")

    def load_forbidden_words(self) -> List[str]:
        if self.forbidden_words_file is None:
            raise ValueError("forbidden_words_file is None")
        with open(self.forbidden_words_file, "r", encoding="utf-8") as file:
            return [word.strip().lower() for word in file if word.strip()]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            await check_message_to_bad_words(
                bot=self.bot, 
                message=event, 
                nlp_model=self.nlp, 
                forbidden_words=self.forbidden_words,
                until_date=self.until_date
            )

            await check_message_to_https_links(
                bot=self.bot,
                message=event,
                nlp_model=self.nlp
            )

        return await handler(event, data)