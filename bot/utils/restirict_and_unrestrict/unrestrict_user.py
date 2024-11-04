from typing import List, Optional

from aiogram import Bot
from aiogram.types import CallbackQuery, Chat, InaccessibleMessage, Message

from ..helpers import unban_with_message, unmute_with_message


async def handle_unmute_for_callback(
    bot: Bot, 
    callback_query: CallbackQuery
    ) -> None:
    if callback_query.message is None or isinstance(callback_query.message, InaccessibleMessage):
        return

    await callback_query.message.delete()

    if callback_query.message.chat is None or callback_query.data is None:
        return

    data_parts: List[str] = callback_query.data.split("_")
    user_id: int = int(data_parts[1])

    user_info = await bot.get_chat_member(
        chat_id=callback_query.message.chat.id, 
        user_id=user_id
    )

    if user_info is None or user_info.user is None:
        return

    await unmute_with_message(
        bot=bot,
        chat_id=callback_query.message.chat.id,
        user_id=user_id,
        message_text=f"<a href='tg://user?id={user_info.user.id}'><b>👀{user_info.user.first_name}</b></a> has been unmuted."
    )


async def handle_unban_for_callback(
    bot: Bot,
    callback_query: CallbackQuery
    ) -> None:
    if callback_query.message is None or isinstance(callback_query.message, InaccessibleMessage):
        return

    await callback_query.message.delete()

    if callback_query.message.chat is None or callback_query.data is None:
        return

    data_parts: List[str] = callback_query.data.split("_")
    user_id: int = int(data_parts[1])

    user_info = await bot.get_chat_member(
        chat_id=callback_query.message.chat.id, 
        user_id=user_id
    )

    if user_info is None or user_info.user is None:
        return

    await unban_with_message(
        bot=bot,
        chat_id=callback_query.message.chat.id,
        user_id=user_id,
        message_text=f"<a href='tg://user?id={user_info.user.id}'><b>👀{user_info.user.first_name}</b></a> has been unbanned."
    )


async def handle_unmute(
    bot: Bot, 
    message: Message
    ) -> None:
    chat: Optional[Chat] = message.chat
    reply: Optional[Message] = message.reply_to_message

    if reply is None or reply.from_user is None or chat is None:
        return

    await unmute_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=reply.from_user.id,
        message_text=f"<a href='tg://user?id={reply.from_user.id}'><b>{reply.from_user.first_name}</b></a> has been unmuted."
    )


async def handle_unban(
    bot: Bot, 
    message: Message
    ) -> None:
    chat: Optional[Chat] = message.chat
    reply: Optional[Message] = message.reply_to_message

    if reply is None or reply.from_user is None or chat is None:
        return

    await unban_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=reply.from_user.id,
        message_text=f"<a href='tg://user?id={reply.from_user.id}'><b>{reply.from_user.first_name}</b></a> has been unbanned."
    )