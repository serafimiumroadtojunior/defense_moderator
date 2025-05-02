from typing import Optional

from aiogram import Bot
from fluentogram import TranslatorRunner
from aiogram.types import (
    CallbackQuery, Chat, 
    User, Message, ChatMember
)

from app.bot.keyboards import ModerationCallback
from ..helpers import (
    unban_with_message, 
    unmute_with_message,
    answer_message
)


async def handle_unmute_for_callback(
    bot: Bot, 
    message: Message, 
    i18n: TranslatorRunner,
    callback: ModerationCallback,
    callback_query: CallbackQuery
) -> None:
    await message.delete()

    user_id: int = callback.user_id
    chat: Chat = message.chat
    admin_user: User = callback_query.from_user
    user_info = await bot.get_chat_member(
        chat_id=chat.id, 
        user_id=user_id
    )

    user: User = user_info.user

    await unmute_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=user.id,
        message_text=i18n.get(
            'unmute-user',
            user_id=user.id,
            user_full_name=user.full_name,
            admin_full_name=admin_user.full_name,
            admin_id=admin_user.id
        )
    )


async def handle_unban_for_callback(
    bot: Bot,
    message: Message,
    i18n: TranslatorRunner,
    callback: ModerationCallback,
    callback_query: CallbackQuery
) -> None:
    await message.delete()

    user_id: int = callback.user_id
    admin_user: User = callback_query.from_user
    chat: Chat = message.chat
    user_info = await bot.get_chat_member(
        chat_id=chat.id, 
        user_id=user_id
    )

    user: User = user_info.user

    await unban_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=user.id,
        message_text=i18n.get(
            'unban-user',
            user_id=user.id,
            user_full_name=user.full_name,
            admin_full_name=admin_user.full_name,
            admin_id=admin_user.id
        )
    )


async def handle_unmute(
    bot: Bot,
    reply_user: User,
    i18n: TranslatorRunner,
    message: Message
) -> None:
    chat: Chat = message.chat
    admin_user: Optional[User] = message.from_user

    if not admin_user:
        await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    await unmute_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=reply_user.id,
        message_text=i18n.get(
            'unmute-user',
            user_id=reply_user.id,
            user_full_name=reply_user.full_name,
            admin_full_name=admin_user.full_name,
            admin_id=admin_user.id
        )
    )


async def handle_unban(
    bot: Bot,
    reply_user: User,
    i18n: TranslatorRunner, 
    message: Message
) -> None:
    chat: Chat = message.chat
    admin_user: Optional[User] = message.from_user

    if not admin_user:
        await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    await unban_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=reply_user.id,
        message_text=i18n.get(
            'unban-user',
            user_id=reply_user.id,
            user_full_name=reply_user.full_name,
            admin_full_name=admin_user.full_name,
            admin_id=admin_user.id
        )
    )