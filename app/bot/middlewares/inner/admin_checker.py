from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware, Bot
from fluentogram import TranslatorRunner
from aiogram.types import (
    CallbackQuery, Chat, 
    Message, TelegramObject,
    InaccessibleMessage)

from app.bot.utils import answer_message, check_admin


class AdminCheckerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            if event.from_user is not None and event.chat is not None:
                bot: Optional[Bot] = data.get('bot')
                chat: Chat = event.chat
                user_id: int = event.from_user.id
                i18n: Optional[TranslatorRunner] = data.get('i18n')

                if not bot or not i18n:
                    return await handler(event, data)
                
                if not await check_admin(
                    bot=bot, 
                    chat_id=chat.id, 
                    user_id=user_id
                ):
                    await answer_message(
                        bot=bot,
                        chat_id=chat.id,
                        text=i18n.get(
                            'error-admins'
                        )
                    )

                return await handler(event, data)
        return await handler(event, data)


class CallbackAdminCheckerMiddleware(AdminCheckerMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:   
        if isinstance(event, CallbackQuery):
            bot: Optional[Bot] = data.get('bot')
            i18n: Optional[TranslatorRunner] = data.get('i18n')

            if not bot or not i18n:
                return await handler(event, data)

            if event.message is None or isinstance(event.message, InaccessibleMessage):
                await event.answer(
                    show_alert=True,
                    text=i18n.get(
                        'error-innacesible'
                    )
                )
                return await handler(event, data)

            user_id: int = event.from_user.id
            chat: Chat = event.message.chat

            if not await check_admin(
                bot=bot, 
                chat_id=chat.id, 
                user_id=user_id
            ):
                await event.answer(
                    show_alert=True,
                    text=i18n.get(
                        'error-button'
                    )
                )
            
            return await handler(event, data)
        return await handler(event, data)