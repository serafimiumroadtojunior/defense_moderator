from typing import Optional

from redis.asyncio.client import Redis
from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram_i18n import I18nContext
from aiogram.types import Chat, Message, User

from app.bot.keyboards import ModerationCallback
from ..helpers import (
    answer_message, ban_with_message, 
    mute_with_message, parse_time_and_reason
)


async def handle_mute(
    bot: Bot, 
    redis: Redis,
    message: Message,
    reply_user: User, 
    command: CommandObject,
    i18n: I18nContext,
    locale: Optional[str]
) -> Message:
    if not message.from_user:
        return await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    if not command.args:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-restrict-args',
                locale
            )
        )

    chat: Chat = message.chat
    admin_user: User = message.from_user
    until_date, reason, readable_time = parse_time_and_reason(
        args=command.args,
        locale=locale,
        i18n=i18n
    )

    return await mute_with_message(
        bot=bot,
        redis=redis,
        locale=locale,
        i18n=i18n,
        chat_id=chat.id,
        user_id=reply_user.id,
        until_date=until_date,
        buttons_level=1,
        button_texts=['Unmute✔️'],
        callback_datas=[
            ModerationCallback(
                action='unmute',
                user_id=reply_user.id
            ).pack()
        ],
        message_text=i18n.get(
            'mute-user',
            locale,
            user_id=reply_user.id,
            user_full_name=reply_user.full_name,
            measure_time=readable_time,
            reason=reason,
            admin_id=admin_user.id,
            admin_full_name=admin_user.full_name
        )
    )


async def handle_ban(
    bot: Bot, 
    message: Message,
    reply_user: User, 
    command: CommandObject,
    i18n: I18nContext,
    locale: Optional[str]
) -> Message:
    if not message.from_user:
        return await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    if not command.args:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-restrict-args',
                locale
            )
        )

    chat: Chat = message.chat
    admin_user: User = message.from_user
    until_date, reason, readable_time = parse_time_and_reason(
        args=command.args,
        locale=locale,
        i18n=i18n
    )

    return await ban_with_message(
        bot=bot,
        locale=locale,
        i18n=i18n,
        chat_id=chat.id,
        user_id=reply_user.id,
        until_date=until_date,
        buttons_level=1,
        button_texts=['Unban✔️'],
        callback_datas=[
            ModerationCallback(
                action='unban',
                user_id=reply_user.id
            ).pack()
        ],
        message_text=i18n.get(
            'ban-user',
            locale,
            user_id=reply_user.id,
            user_full_name=reply_user.full_name,
            measure_time=readable_time,
            reason=reason,
            admin_id=admin_user.id,
            admin_full_name=admin_user.full_name
        )
    )