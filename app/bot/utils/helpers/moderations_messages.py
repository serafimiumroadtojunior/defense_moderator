import asyncio
from datetime import datetime
from typing import Optional, List

from aiogram import Bot
from fluentogram import TranslatorRunner
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions

from .message_functions import answer_message, send_unrestriction_message
from app.bot.database import add_mute_flag, drop_mute_flag


async def unban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    i18n: TranslatorRunner
) -> None:
    try:
        await bot.unban_chat_member(
            chat_id=chat_id, 
            user_id=user_id
        )

    except TelegramBadRequest:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat_id,
            text=i18n.get(
                'error-unban'
            )
        )
        return None

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
    )


async def unmute_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    i18n: TranslatorRunner
) -> None:
    try:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=True)
        )

    except TelegramBadRequest:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat_id,
            text=i18n.get(
                'error-unmute'
            )
        )
        return None

    await drop_mute_flag(
        chat_id=chat_id,
        user_id=user_id
    )

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text
    )


async def ban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    i18n: TranslatorRunner,
    button_texts: Optional[List[str]] = None,
    callback_datas: Optional[List[str]] = None,
    until_date: Optional[datetime] = None,
    buttons_level: Optional[int] = None
) -> None:
    try:
        await bot.ban_chat_member(
            chat_id=chat_id, 
            user_id=user_id, 
            until_date=until_date
        )

    except TelegramBadRequest:
        await answer_message(
            bot=bot,
            chat_id=chat_id,
            text=i18n.get(
                'error-ban'
            )
        )
        return None

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
            i18n=i18n,
            chat_id=chat_id,
            user_id=user_id, 
            new_datetime=until_date
        )
    )

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        buttons_level=buttons_level,
        button_texts=button_texts,
        callback_datas=callback_datas
    )


async def mute_with_message(
    bot: Bot, 
    chat_id: int,
    user_id: int,  
    message_text: str,
    i18n: TranslatorRunner,
    button_texts: Optional[List[str]] = None,
    callback_datas: Optional[List[str]] = None,
    until_date: Optional[datetime] = None,
    buttons_level: Optional[int] = None
) -> None:
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
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat_id,
            text=i18n.get(
                'error-mute'
            )
        )
        return None

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
            i18n=i18n,
            chat_id=chat_id, 
            user_id=user_id, 
            new_datetime=until_date
        )
    )

    await add_mute_flag(
        user_id=user_id,
        chat_id=chat_id,
        until_date=until_date
    )

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        buttons_level=buttons_level,
        button_texts=button_texts,
        callback_datas=callback_datas
    )