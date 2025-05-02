from typing import (
    Any, Awaitable, 
    Callable, Dict,
    Optional
)

from fluentogram import TranslatorRunner
from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, Update,
    ChatMemberUpdated, User
)

from app.bot.utils import answer_message


class GoodbyeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat_member:
            i18n: Optional[TranslatorRunner] = data.get('i18n')
            bot: Optional[Bot] = data.get('bot')
            member: ChatMemberUpdated = event.chat_member
            chat_id: int = member.chat.id
            new_member = member.new_chat_member
            old_member = member.old_chat_member

            if not bot or not i18n:
                return await handler(event, data)

            if new_member.status == "left" or old_member.status == "left":
                user: User = member.from_user

                await answer_message(
                    bot=bot,
                    chat_id=chat_id,
                    text=i18n.get(
                    'goodbye-message',
                    user_name=user.full_name,
                    user_id=user.id
                    )   
                )

        return await handler(event, data)