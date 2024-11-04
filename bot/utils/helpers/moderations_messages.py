import asyncio
from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from .message_functions import answer_message, send_unrestriction_message
from .modetate_functions import ban_user, mute_user, unban_user, unmute_user


async def unban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str
    ) -> None:
    try:
        await unban_user(
            bot=bot, 
            user_id=user_id, 
            chat_id=chat_id
        )
        
    except TelegramBadRequest:
        await answer_message(
            bot=bot,
            chat_id=chat_id,
            text="<b>Error unban!</b>",
        )

    await answer_message(
        bot=bot,
        chat_id=chat_id,
        text=message_text,
        delay=30
    )
    return


async def unmute_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str
    ) -> None:
    try:
        await unmute_user(
            bot=bot, 
            user_id=user_id, 
            chat_id=chat_id       
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
    return


async def ban_with_message(
    bot: Bot, 
    chat_id: int, 
    user_id: int,
    message_text: str,
    until_date: Optional[datetime] = None
    ) -> None:
    try:
        await ban_user(
            bot=bot, 
            user_id=user_id, 
            chat_id=chat_id, 
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
    return


async def mute_with_message(
    bot: Bot, 
    chat_id: int,
    user_id: int,  
    message_text: str,
    until_date: Optional[datetime] = None
    ) -> None:
    try:
        await mute_user(
            bot=bot, 
            user_id=user_id, 
            chat_id=chat_id, 
            until_date=until_date
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
    return