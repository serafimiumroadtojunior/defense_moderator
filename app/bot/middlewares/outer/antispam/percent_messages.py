from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, TelegramObject

from app.bot.utils import parse_messages_percent


class PercentSpamParseMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot) -> None:
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat_member:
            await parse_messages_percent(
                bot=self.bot,
                member=event.chat_member,
                spam_percent=65.0
            )

        return await handler(event, data)