from typing import Any, Awaitable, Callable, Dict, Optional

from redis.asyncio.client import Redis
from aiogram import BaseMiddleware, Bot
from aiogram_i18n import I18nContext
from aiogram.types import (
    CallbackQuery, Chat, 
    Message, TelegramObject,
    InaccessibleMessage
)

from app.bot.utils import answer_message, check_admin
from app.bot.database import get_chat_locale


class AdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, bot: Bot):
        self.redis: Redis = redis
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            if event.from_user and event.chat:
                chat: Chat = event.chat
                user_id: int = event.from_user.id
                i18n: Optional[I18nContext] = data.get('i18n')

                if not i18n:
                    return await handler(event, data)
                
                if not await check_admin(
                    bot=self.bot, 
                    chat_id=chat.id, 
                    user_id=user_id
                ):
                    locale: Optional[str] = await get_chat_locale(
                        chat_id=chat.id,
                        redis=self.redis
                    )

                    await answer_message(
                        bot=self.bot,
                        chat_id=chat.id,
                        text=i18n.get(
                            'error-admins',
                            locale
                        )
                    )

                return await handler(event, data)
        return await handler(event, data)


class CallbackAdminCheckerMiddleware(AdminCheckerMiddleware):
    def __init__(self, redis: Redis, bot: Bot):
        self.redis: Redis = redis
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:   
        if isinstance(event, CallbackQuery):
            i18n: Optional[I18nContext] = data.get('i18n')

            if not i18n:
                return await handler(event, data)

            if not isinstance(event.message, Message):
                await event.answer(
                    show_alert=True,
                    text=i18n.get(
                        'error-innacesible'
                    )
                )
                return await handler(event, data)

            user_id: int = event.from_user.id
            chat: Chat = event.message.chat
            locale: Optional[str] = await get_chat_locale(
                chat_id=event.message.chat.id,
                redis=self.redis
            )

            if not await check_admin(
                bot=self.bot, 
                chat_id=chat.id, 
                user_id=user_id
            ):
                await event.answer(
                    show_alert=True,
                    text=i18n.get(
                        'error-button',
                        locale
                    )
                )
            
            return await handler(event, data)
        return await handler(event, data)