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
    if not message.reply_to_message or not message.chat:
        return

    if not message.from_user or not message.reply_to_message.from_user:
        return

    if not command.args:
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
        action='unmute',
        until_date=until_date,
        message_text=(
            f'<a href="tg://user?id={reply_user.id}"><b>👀{reply_user.full_name}</b></a> has been muted for {readable_time}' 
            f'\nfor the reason: {reason}. \nAdmin: <a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
        )
    )


async def handle_ban(
    bot: Bot, 
    message: Message, 
    command: CommandObject
) -> None:
    if not message.reply_to_message or not message.chat:
        return

    if not message.from_user or not message.reply_to_message.from_user:
        return

    if not command.args:
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

    await ban_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=reply_user.id,
        action='unban',
        until_date=until_date,
        message_text=(
            f'<a href="tg://user?id={reply_user.id}"><b>👀{reply_user.full_name}</b></a> has been baned for {readable_time}' 
            f'\nfor the reason: {reason}. \nAdmin: <a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
        )
    )