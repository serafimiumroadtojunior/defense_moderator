from typing import (
    Any, Awaitable, 
    Callable, Dict
)

from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, Update,
    ChatMemberUpdated
)

from app.bot.utils import answer_message


class GoodbyeMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat_member:
            member: ChatMemberUpdated = event.chat_member
            chat_id: int = member.chat.id
            new_member = member.new_chat_member
            old_member = member.old_chat_member

            if new_member.status == "left" or old_member.status == "left":
                user_name: str = member.from_user.full_name
                text: str = f"😞Goodbye {user_name}. Hope you come back again!"

                await answer_message(
                    bot=self.bot,
                    chat_id=chat_id,
                    text=text,
                    delay=30
                )

        return await handler(event, data)