from typing import Optional

from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.types import Chat, Message

from ..helpers import (answer_message, ban_with_message, mute_with_message,
                       parse_time_and_reason)


async def handle_mute(
    bot: Bot, 
    message: Message, 
    command: CommandObject
    ) -> None:
    chat: Optional[Chat] = message.chat
    reply: Optional[Message] = message.reply_to_message

    if reply is None or chat is None:
        return

    if command.args is None:
        await answer_message(
            bot=bot,
            chat_id=chat.id,
            text="🔴Error! Provide time and reason in the command."
        )
        return

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

    if reply.from_user is None or message.from_user is None:
        return
    
    await mute_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=reply.from_user.id,
        until_date=until_date,
        message_text=f"👀<a href='tg://user?id={reply.from_user.id}'><b>{reply.from_user.first_name}</b></a> has been muted for {readable_time}" 
        f"\nfor the reason: {reason}. \nAdmin: <a href='tg://user?id={message.from_user.id}'><b>{message.from_user.first_name}</b></a>"
    )


async def handle_ban(
    bot: Bot, 
    message: Message, 
    command: CommandObject
    ) -> None:
    chat: Optional[Chat] = message.chat
    reply: Optional[Message] = message.reply_to_message

    if reply is None or chat is None:
        return

    if command.args is None:
        await answer_message(
            bot=bot,
            chat_id=chat.id,
            text="🔴Error! Provide time and reason in the command."
        )
        return

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

    if reply.from_user is None or message.from_user is None:
        return

    await ban_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=reply.from_user.id,
        until_date=until_date,
        message_text=f"👀<a href='tg://user?id={reply.from_user.id}'><b>{reply.from_user.first_name}</b></a> has been baned for {readable_time}" 
        f"\nfor the reason: {reason}. \nAdmin: <a href='tg://user?id={message.from_user.id}'><b>{message.from_user.first_name}</b></a>"
    )