from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware
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
            rules_message_id: Optional[int] = await get_message_id(
                chat_id=chat.id
            )

            if not chat.type == 'channel':
                return await handler(event, data)

            if rules_message_id:
                await event.reply(
                    text=(
                        "<b>That new post! Please, read the</b>"
                        f" <a href='https://t.me/{chat.id}/{rules_message_id}'>rules</a>."
                    )
                )

            return await handler(event, data)
        return await handler(event, data)