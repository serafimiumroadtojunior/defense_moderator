from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from fluentogram import TranslatorHub

from app.bot.database import get_chat_locale


class TranslatorRunnerMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, Message):
            return await handler(event, data)

        hub: TranslatorHub = data.get('_translator_hub')
        chat_locale: str = await get_chat_locale(event.chat.id)

        data['i18n'] = hub.get_translator_by_locale(chat_locale)
        return await handler(event, data)
