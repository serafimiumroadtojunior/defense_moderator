from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
from fluentogram import TranslatorRunner
from aiogram.types import TelegramObject, Message, Chat

from app.bot.database import get_message_id


class ChannelPostMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.is_automatic_forward:
            chat: Chat = event.chat
            i18n: TranslatorRunner = data.get('i18n')
            rules_message_id: Optional[int] = await get_message_id(
                chat_id=chat.id
            )

            if not chat.type == 'channel':
                return await handler(event, data)
            
            if not i18n:
                return await handler(event, data)

            if rules_message_id:
                await event.reply(
                    text=i18n.get(
                        "new-post",
                        chat_id=chat.id,
                        rules_id=rules_message_id
                    )
                )

            return await handler(event, data)
        return await handler(event, data)