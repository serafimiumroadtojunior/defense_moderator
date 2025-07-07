import asyncio
from datetime import datetime
from typing import Optional, Sequence

from redis.asyncio.client import Redis
from aiogram import Bot
from aiogram_i18n import I18nContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions, Message

from .message_functions import answer_message, send_unrestriction_message
from app.bot.database import add_mute_flag, drop_mute_flag


async def unban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    i18n: I18nContext,
    locale: Optional[str] = None
) -> Message:
    try:
        await bot.unban_chat_member(
            chat_id=chat_id, 
            user_id=user_id
        )

    except TelegramBadRequest:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat_id,
            text=i18n.get(
                'error-unban',
                locale
            )
        )

    return await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
    )


async def unmute_with_message(
    bot: Bot, 
    redis: Redis,
    chat_id: int, 
    user_id: int,
    message_text: str,
    i18n: I18nContext,
    locale: Optional[str] = None
) -> Message:
    try:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )

    except TelegramBadRequest:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat_id,
            text=i18n.get(
                'error-unmute',
                locale
            )
        )

    await drop_mute_flag(
        chat_id=chat_id,
        user_id=user_id
    )

    return await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text
    )


async def ban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    i18n: I18nContext,
    locale: Optional[str] = None,
    button_texts: Optional[Sequence[str]] = None,
    callback_datas: Optional[Sequence[str]] = None,
    until_date: Optional[datetime] = None,
    buttons_level: Optional[int] = None
) -> Message:
    try:
        await bot.ban_chat_member(
            chat_id=chat_id, 
            user_id=user_id, 
            until_date=until_date
        )

    except TelegramBadRequest:
        return await answer_message(
            bot=bot,
            chat_id=chat_id,
            text=i18n.get(
                'error-ban',
                locale
            )
        )

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
            locale=locale,
            i18n=i18n,
            chat_id=chat_id,
            user_id=user_id, 
            new_datetime=until_date
        )
    )

    return await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        buttons_level=buttons_level,
        button_texts=button_texts,
        callback_datas=callback_datas
    )


async def mute_with_message(
    bot: Bot, 
    redis: Redis,
    chat_id: int,
    user_id: int,  
    message_text: str,
    i18n: I18nContext,
    locale: Optional[str] = None,
    button_texts: Optional[Sequence[str]] = None,
    callback_datas: Optional[Sequence[str]] = None,
    until_date: Optional[datetime] = None,
    buttons_level: Optional[int] = None
) -> Message:
    try:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            until_date=until_date,
            permissions=ChatPermissions(
                can_send_messages=False
            )
        )

    except TelegramBadRequest:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat_id,
            text=i18n.get(
                'error-mute',
                locale
            )
        )

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
            locale=locale,
            i18n=i18n,
            chat_id=chat_id, 
            user_id=user_id, 
            new_datetime=until_date
        )
    )

    await add_mute_flag(
        redis=redis,
        user_id=user_id,
        chat_id=chat_id,
        until_date=until_date
    )

    return await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        buttons_level=buttons_level,
        button_texts=button_texts,
        callback_datas=callback_datas
    )