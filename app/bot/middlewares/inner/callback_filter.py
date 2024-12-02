from typing import Any, Awaitable, Callable, Dict, List

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject


class CallbackFilterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, CallbackQuery):
            if event.data and isinstance(event.data, str):
                callback_data: List[str] = event.data.split('_')
                user_id: int = int(callback_data[1])

            if event.from_user:
                if user_id != event.from_user.id:
                    await event.answer("It’s not good to touch other people’s buttons!", show_alert=True)
                    return

            return await handler(event, data)
        return await handler(event, data)