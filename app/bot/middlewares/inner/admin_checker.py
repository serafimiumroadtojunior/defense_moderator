from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware, Bot
from aiogram.types import CallbackQuery, Chat, Message, TelegramObject

from app.bot.utils import answer_message, check_admin


class AdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            if event.from_user is not None and event.chat is not None:
                user_id: int = event.from_user.id
                
                if not await check_admin(self.bot, event.chat.id, user_id):
                    await answer_message(
                        bot=self.bot,
                        chat_id=event.chat.id,
                        text="You do not have sufficient rights to perform this function.",
                        delay=30
                    )

                return await handler(event, data)
        return await handler(event, data)


class CallbackAdminCheckerMiddleware(AdminCheckerMiddleware):
    def __init__(self, bot: Bot):
        super().__init__(bot=bot)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:   
        if isinstance(event, CallbackQuery):
            if event.message is None:
                await event.answer(
                    "The message related to this action is not available.",
                    show_alert=True,
                )
                return

            user_id: int = event.from_user.id
            chat: Chat = event.message.chat

            if not await check_admin(bot=self.bot, chat_id=chat.id, user_id=user_id):
                await event.answer(
                    "You do not have sufficient rights to perform this function.",
                    show_alert=True
                )
            
            return await handler(event, data)
        return await handler(event, data)