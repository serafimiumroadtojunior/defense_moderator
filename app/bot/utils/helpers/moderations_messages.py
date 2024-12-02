import asyncio
from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ChatPermissions

from .message_functions import answer_message, send_unrestriction_message


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
        callback_data=f"unban_{user_id}",
        button_text='Unban',
        delay=30
    )


async def mute_with_message(
    bot: Bot, 
    chat_id: int,
    user_id: int,  
    message_text: str,
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

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        callback_data=f"unmute_{user_id}",
        button_text='Unmute',
        delay=30
    )