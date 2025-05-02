from typing import Any, Awaitable, Callable, Dict, List, Optional

from aiogram import BaseMiddleware
from fluentogram import TranslatorRunner
from aiogram.types import CallbackQuery, TelegramObject


class CallbackFilterMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, CallbackQuery):  
            if event.data: 
                callback_data: List[str] = event.data.split(':')
                i18n: Optional[TranslatorRunner] = data.get('i18n')  
                if len(callback_data) > 2: 
                    user_id = int(callback_data[2]) 

                    if not i18n:
                        return await handler(event, data)

                    if event.from_user and user_id != event.from_user.id:
                        await event.answer(
                            show_alert=True,
                            text=i18n.get(
                                'error-button'
                            )
                        )

        return await handler(event, data)