from typing import Callable, Awaitable, Dict, Any, List

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, Chat


class CheckGroupMiddleware(BaseMiddleware):
    def __init__(self):
        self.groups_type: List[str] = [
            "group", 
            "channel", 
            "supergroup"
        ]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message) and event.chat:
            chat: Chat = event.chat

            if chat.type in self.groups_type:
                return await handler(event, data)

            return None