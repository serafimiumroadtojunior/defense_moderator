from typing import Any, Awaitable, Callable, Dict, List, Optional, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, TelegramObject, User

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
        if isinstance(event, Message):
            if not event.chat:
                return await handler(event, data)
            
            chat_id: int = event.chat.id
            chat_name: Optional[Union[str, int]] = event.chat.username if event.chat.username else chat_id
            new_chat_members: Optional[List[User]] = event.new_chat_members
            rules_message_id: Optional[int] = await get_message_id_by_chat_id(chat_id=chat_id)

            if new_chat_members:
                for new_member in new_chat_members:
                    user_name: str = new_member.first_name
                    
                    rules_url: str = f"https://t.me/{chat_name}/{rules_message_id}"
                    text: str = f"👀<b>Welcome {user_name}!</b>\nBefore writing in the chat, we recommend that you read the <a href='{rules_url}'><b>rules</b></a>."

                    await mute_with_message(
                        bot=self.bot,
                        chat_id=event.chat.id,
                        user_id=new_member.id,
                        message_text=text
                    )

        return await handler(event, data)