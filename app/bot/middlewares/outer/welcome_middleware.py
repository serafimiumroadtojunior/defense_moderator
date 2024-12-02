from typing import (
    Any, Awaitable, Callable,
    Dict, Optional
)

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, ChatMemberUpdated

from app.bot.database import get_message_id_by_chat_id
from app.bot.utils import mute_with_message


class WelcomeMiddleware(BaseMiddleware):
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

            if new_member.status == "member" or old_member.status == "member":
                user_name: str = event.from_user.full_name
                rules_message_id: Optional[int] = await get_message_id_by_chat_id(chat_id=chat_id)
                
                rules_url: str = f"https://t.me/{chat_id}/{rules_message_id}"
                text: str = (
                    f"👀<b>Welcome {user_name}!</b>\n"
                    "Before writing in the chat," 
                    f"we recommend that you read the <a href='{rules_url}'><b>rules</b></a>."
                )

                await mute_with_message(
                    bot=self.bot,
                    chat_id=chat_id,
                    user_id=event.from_user.id,
                    message_text=text
                )

        return await handler(event, data)