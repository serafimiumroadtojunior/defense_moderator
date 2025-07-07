from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from spacy.language import Language
from spacy import load
from spacy.tokens import Doc

from app.bot.database import add_message


class StatsSpamMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        self.nlp: Language = load("ru_core_news_sm")

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            if event.from_user and event.text:
                doc: Doc = self.nlp(event.text)
                message_text: str = " ".join([token.lemma_ for token in doc])

                await add_message(
                    user_id=event.from_user.id,
                    message=message_text
                )

            return await handler(event, data)
        return await handler(event, data)