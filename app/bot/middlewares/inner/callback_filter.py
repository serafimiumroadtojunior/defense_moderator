from typing import Any, Awaitable, Callable, Dict, Optional

from redis.asyncio.client import Redis
from aiogram import BaseMiddleware
from aiogram_i18n import I18nContext
from aiogram.types import (
    CallbackQuery, TelegramObject, 
    Message
)

from app.bot.database import get_chat_locale
from app.bot.keyboards import ModerationCallback


class CallbackFilterMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis):
        self.redis: Redis = redis

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, CallbackQuery):  
            if event.data: 
                i18n: Optional[I18nContext] = data.get('i18n')
                callback: ModerationCallback = ModerationCallback.unpack(event.data) 

                if not i18n:
                    return await handler(event, data)
                
                if not isinstance(event.message, Message):
                    return await handler(event, data)      

                if callback.user_id != event.from_user.id:
                    locale: Optional[str] =  await get_chat_locale(
                        redis=self.redis,
                        chat_id=event.message.chat.id
                    )

                    await event.answer(
                        show_alert=True,
                        text=i18n.get(
                            'error-button',
                            locale
                        )
                    )

            return await handler(event, data)
        return await handler(event, data)