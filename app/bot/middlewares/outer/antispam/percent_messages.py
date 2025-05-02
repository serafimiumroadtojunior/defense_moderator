from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from fluentogram import TranslatorRunner
from aiogram.types import Update, TelegramObject

from app.bot.utils import parse_messages_percent


class PercentSpamParseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        i18n: TranslatorRunner = data.get('i18n')
        bot: Bot = data.get('bot')

        if not bot or not i18n:
            return await handler(event, data)

        if event.chat_member:
            await parse_messages_percent(
                bot=bot,
                i18n=i18n,
                member=event.chat_member
            )

        return await handler(event, data)