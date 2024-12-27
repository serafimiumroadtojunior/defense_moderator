from typing import Optional

from aiogram import Bot
from aiogram.types import (
    CallbackQuery, Chat, 
    User, Message
)

from ..helpers import (
    unban_with_message, 
    unmute_with_message,
    ModerationCallback
)


async def handle_unmute_for_callback(
    bot: Bot, 
    callback: ModerationCallback,
    callback_query: CallbackQuery
) -> None:
    if not isinstance(callback_query.message, Message):
        return

    if callback_query.message.chat is None:
        return

    await callback_query.message.delete()

    user_id: int = callback.user_id
    chat: Chat = callback_query.message.chat
    user_info = await bot.get_chat_member(
        chat_id=chat.id, 
        user_id=user_id
    )

    user: User = user_info.user

    await unmute_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=user.id,
        message_text=(
            f"<a href='tg://user?id={user.id}'><b>👀{user.full_name}</b></a>"
            "has been unmuted."
        )
    )


async def handle_unban_for_callback(
    bot: Bot,
    callback: ModerationCallback,
    callback_query: CallbackQuery
) -> None:
    if not isinstance(callback_query.message, Message):
        return

    if callback_query.message.chat is None:
        return

    await callback_query.message.delete()

    user_id: int = callback.user_id
    chat: Chat = callback_query.message.chat
    user_info = await bot.get_chat_member(
        chat_id=chat.id, 
        user_id=user_id
    )

    user: User = user_info.user

    await unban_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=user.id,
        message_text=(
            f"<a href='tg://user?id={user.id}'><b>👀{user.full_name}</b></a>"
            "has been unbanned."
        )
    )


async def handle_unmute(
    bot: Bot, 
    message: Message
) -> None:
    chat: Optional[Chat] = message.chat
    reply: Optional[Message] = message.reply_to_message
    user: Optional[User] = reply.from_user

    if reply is None or reply.from_user is None:
        return 

    if chat is None:
        return

    await unmute_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=user.id,
        message_text=(
            f"<a href='tg://user?id={user.id}'><b>{user.full_name}</b></a>" 
            "has been unmuted."
        )
    )


async def handle_unban(
    bot: Bot, 
    message: Message
) -> None:
    chat: Optional[Chat] = message.chat
    reply: Optional[Message] = message.reply_to_message
    user: Optional[User] = reply.from_user

    if reply is None or reply.from_user is None:
        return

    if chat is None:
        return

    await unban_with_message(
        bot=bot,
        chat_id=chat.id,
        user_id=user.id,
        message_text=(
            f"<a href='tg://user?id={user.id}'><b>{user.full_name}</b></a>"
            "has been unbanned."
        )
    )