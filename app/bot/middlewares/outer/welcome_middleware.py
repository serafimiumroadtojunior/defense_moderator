from typing import (
    Any, Awaitable, Callable,
    Dict, Optional
)

from redis.asyncio.client import Redis
from aiogram_i18n import I18nContext
from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    TelegramObject, ChatMemberUpdated, 
    User, Update
)

from app.bot.keyboards import ModerationCallback
from app.bot.database import get_rules_id, get_chat_locale
from app.bot.utils import mute_with_message


class WelcomeMiddleware(BaseMiddleware):
    def __init__(self, redis: Redis, bot: Bot):
        self.redis: Redis = redis
        self.bot: Bot = bot

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat_member:
            i18n: Optional[I18nContext] = data.get('i18n')
            member: ChatMemberUpdated = event.chat_member
            chat_id: int = member.chat.id
            new_member = member.new_chat_member
            old_member = member.old_chat_member

            if not i18n:
                return await handler(event, data)

            if new_member.status == "member" or old_member.status == "member":
                user: User = member.from_user
                rules_message_id: Optional[int] = await get_rules_id(
                    chat_id=chat_id,
                    redis=self.redis
                )
                locale: Optional[str] = await get_chat_locale(
                    chat_id=chat_id,
                    redis=self.redis
                )

                await mute_with_message(
                    bot=self.bot,
                    i18n=i18n,
                    redis=self.redis,
                    locale=locale,
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
                        locale,
                        user_name=user.full_name,
                        rules_id=rules_message_id,
                        chat_id=chat_id,
                        user_id=user.id
                    )
                )

            return await handler(event, data)
        return await handler(event, data)