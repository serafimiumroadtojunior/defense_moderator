from typing import (
    Any, Awaitable, Callable,
    Dict, Optional
)

from fluentogram import TranslatorRunner
from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, ChatMemberUpdated, 
    User, Update
)

from app.bot.keyboards import ModerationCallback
from app.bot.database import get_message_id
from app.bot.utils import mute_with_message


class WelcomeMiddleware(BaseMiddleware):
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

            if new_member.status == "member" or old_member.status == "member":
                rules_message_id: Optional[int] = await get_message_id(chat_id=chat_id)
                user: User = member.from_user

                await mute_with_message(
                    bot=bot,
                    i18n=i18n,
                    chat_id=chat_id,
                    user_id=user.id,
                    buttons_level=1,
                    button_texts=['Complete captcha'],
                    callback_datas=[
                        ModerationCallback(
                            action='captcha',
                            user_id=user.id
                        ).pack()
                    ],
                    message_text=i18n.get(
                        'welcome_message',
                        user_name=user.full_name,
                        rules_id=rules_message_id,
                        chat_id=chat_id,
                        user_id=user.id
                    )
                )

        return await handler(event, data)