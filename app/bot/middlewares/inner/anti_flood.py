from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from cachetools import TTLCache


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = 5) -> None:
        super().__init__()
        self.limit: TTLCache = TTLCache(maxsize=10_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, Message):
            if event.chat.id in self.limit:
                return
            else:
                self.limit[event.chat.id] = None
        return await handler(event, data)