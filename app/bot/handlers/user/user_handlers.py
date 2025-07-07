from typing import Optional
from datetime import datetime

from redis.asyncio.client import Redis
from aiogram import Bot, F, Router
from aiogram_i18n import I18nContext
from aiogram.types import CallbackQuery, Message, User, Chat
from aiogram.filters import Command, CommandObject

from app.bot.keyboards import ModerationCallback
from app.bot.database import get_mute_flag, get_chat_locale
from app.bot.utils import (
    unmute_with_message, mute_with_message,
    report_user, answer_message
)

user_router: Router = Router()

@user_router.callback_query(ModerationCallback.filter(F.action == 'captcha'))
async def captcha_complete(
    callback_query: CallbackQuery,
    redis: Redis,
    i18n: I18nContext,
    bot: Bot
) -> Optional[Message]:
    if not isinstance(callback_query.message, Message):
        return None

    await callback_query.message.delete()

    user: User = callback_query.from_user
    chat_id: int = callback_query.message.chat.id
    mute_flag: Optional[datetime] = await get_mute_flag(
        user_id=user.id,
        chat_id=chat_id
    )
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat_id,
        redis=redis
    )

    if not mute_flag:
        return await unmute_with_message(
            bot=bot,
            redis=redis,
            i18n=i18n,
            chat_id=chat_id,
            user_id=user.id,
            message_text=i18n.get(
                'complete-captcha',
                locale,
                user_id=user.id,
                user_full_name=user.full_name
            )
        )

    return await mute_with_message(
        bot=bot,
        redis=redis,
        i18n=i18n,
        chat_id=chat_id,
        user_id=user.id,
        until_date=mute_flag,
        buttons_level=1,
        button_texts=[
            i18n.get(
                'unmute-button',
                locale
            )
        ],
        callback_datas=[
            ModerationCallback(
                action='unmute',
                user_id=user.id
            ).pack()
        ],
        message_text=i18n.get(
            'abuse-welcome',
            locale,
            user_id=user.id,
            user_full_name=user.full_name
        )
    )


@user_router.message(Command('report'))
async def report_command(
    bot: Bot,
    redis: Redis,
    message: Message, 
    i18n: I18nContext,
    command: CommandObject
) -> Optional[Message]:
    reply: Optional[Message] = message.reply_to_message
    chat: Chat = message.chat
    locale: Optional[str] = await get_chat_locale(
        redis=redis,
        chat_id=chat.id
    )

    if not reply or not reply.from_user:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    reply_user: User = reply.from_user

    return await report_user(
        message=message,
        reply=reply,
        locale=locale,
        reply_user=reply_user,
        command=command,
        i18n=i18n,
        bot=bot
    )