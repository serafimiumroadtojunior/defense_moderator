from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Chat, Message, User

from ..helpers import (
    answer_message, ban_with_message, 
    mute_with_message, parse_time_and_reason
)


async def handle_mute(
    bot: Bot, 
    message: Message, 
    command: CommandObject
) -> None:
    if message.reply_to_message is None or message.chat is None:
        return
    
    if message.from_user is None or message.reply_to_message.from_user is None:
        return
    
    if command.args is None:
        await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text="🔴Error! Provide time and reason in the command."
        )
        return
    
    chat: Chat = message.chat
    reply_user: User = message.reply_to_message.from_user
    user: User = message.from_user

    until_date, reason, readable_time = parse_time_and_reason(
        args=command.args
    )
    
    await mute_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=reply_user.id,
        until_date=until_date,
        message_text=f'<a href="tg://user?id={reply_user.id}"><b>👀{reply_user.full_name}</b></a> has been muted for {readable_time}' 
        f'\nfor the reason: {reason}. \nAdmin: <a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
    )


async def handle_ban(
    bot: Bot, 
    message: Message, 
    command: CommandObject
) -> None:
    if message.reply_to_message is None or message.chat is None:
        return
    
    if message.from_user is None or message.reply_to_message.from_user is None:
        return
    
    if command.args is None:
        await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text="🔴Error! Provide time and reason in the command."
        )
        return
    
    chat: Chat = message.chat
    reply_user: User = message.reply_to_message.from_user
    user: User = message.from_user

    until_date, reason, readable_time = parse_time_and_reason(
        args=command.args
    )

    if until_date is None:
        await answer_message(
            bot=bot,
            chat_id=chat.id,
            text="🔴Error! Could not parse the time. Correct format: /mute 12h for spam"
        )
        return

    await ban_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=reply_user.id,
        until_date=until_date,
        message_text=f'<a href="tg://user?id={reply_user.id}"><b>👀{reply_user.full_name}</b></a> has been baned for {readable_time}' 
        f'\nfor the reason: {reason}. \nAdmin: <a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
    )