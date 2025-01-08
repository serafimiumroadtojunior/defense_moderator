import asyncio
from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions

from .message_functions import answer_message, send_unrestriction_message
from app.bot.database import add_mute_flag, drop_mute_flag


async def unban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str
) -> None:
    try:
        await bot.unban_chat_member(
            chat_id=chat_id, 
            user_id=user_id
        )

    except TelegramBadRequest:
        await answer_message(
            bot=bot,
            chat_id=chat_id,
            text="<b>Error unban!</b>",
        )
        return

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        delay=30
    )


async def unmute_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str
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
            chat_id=chat_id,
            text="<b>Error unmute!</b>",
        )
        return

    await drop_mute_flag(
        chat_id=chat_id,
        user_id=user_id
    )

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        delay=30
    )


async def ban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    button_text: Optional[str] = 'Unban',
    action: Optional[str] = None,
    until_date: Optional[datetime] = None
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
            text="<b>Error ban!</b>",
        )
        return

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
            chat_id=chat_id,
            user_id=user_id, 
            new_datetime=until_date
        )
    )

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        action=action,
        user_id=user_id,
        button_text=button_text,
        delay=30
    )


async def mute_with_message(
    bot: Bot, 
    chat_id: int,
    user_id: int,  
    message_text: str,
    button_text: Optional[str] = 'Unmute',
    action: Optional[str] = None,
    until_date: Optional[datetime] = None
) -> None:
    try:
        await bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date,
        )

    except TelegramBadRequest:
        await answer_message(
            bot=bot,
            chat_id=chat_id,
            text="<b>Error mute!</b>",
        )
        return

    asyncio.create_task(
        send_unrestriction_message(
            bot=bot, 
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
        user_id=user_id,
        action=action,
        button_text=button_text,
        delay=30
    )