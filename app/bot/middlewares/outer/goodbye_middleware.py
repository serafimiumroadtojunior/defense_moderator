from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject, User

from app.bot.utils import answer_message


class GoodbyeMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, Message):
            if not event.chat:
                return await handler(event, data)

            chat_id: int = event.chat.id
            left_chat_member: Optional[User] = event.left_chat_member

            if left_chat_member:
                user_name: str = left_chat_member.first_name

                text: str = f"😞Goodbye {user_name}. Hope you come back again!"

                await answer_message(
                    bot=self.bot,
                    chat_id=chat_id,
                    text=text,
                    delay=30
                )

        return await handler(event, data)