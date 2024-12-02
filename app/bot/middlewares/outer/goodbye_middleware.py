from typing import (
    Any, Awaitable, 
    Callable, Dict
)

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, ChatMemberUpdated

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
        if isinstance(event, ChatMemberUpdated):
            chat_id: int = event.chat.id
            new_member = event.new_chat_member
            old_member = event.old_chat_member

            if new_member.status == "left" or old_member.status == "left":
                user_name: str = event.from_user.full_name
                text: str = f"😞Goodbye {user_name}. Hope you come back again!"

                await answer_message(
                    bot=self.bot,
                    chat_id=chat_id,
                    text=text,
                    delay=30
                )

        return await handler(event, data)