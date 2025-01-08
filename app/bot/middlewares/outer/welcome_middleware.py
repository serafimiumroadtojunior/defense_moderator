from typing import (
    Any, Awaitable, Callable,
    Dict, Optional
)

from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, ChatMemberUpdated, 
    User, Update
)

from app.bot.database import get_message_id
from app.bot.utils import mute_with_message


class WelcomeMiddleware(BaseMiddleware):
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

            if new_member.status == "member" or old_member.status == "member":
                rules_message_id: Optional[int] = await get_message_id(chat_id=chat_id)
                user: User = member.from_user

                rules_url: str = f"https://t.me/{chat_id}/{rules_message_id}"
                text: str = (
                    f"👀<b>Welcome {user.full_name}!</b>\n"
                    "Before writing in the chat," 
                    f"we recommend that you read the <a href='{rules_url}'><b>rules</b></a>."
                )

                await mute_with_message(
                    bot=self.bot,
                    chat_id=chat_id,
                    user_id=user.id,
                    action='captcha',
                    button_text='Complete captcha',
                    message_text=text
                )

        return await handler(event, data)