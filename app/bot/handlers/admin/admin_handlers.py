import re
from typing import Optional, Union

from redis.asyncio.client import Redis
from aiogram_i18n import I18nContext
from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    CallbackQuery, Chat, 
    Message, User, MaybeInaccessibleMessage
)

from app.bot.config import Locale
from app.bot.keyboards import ModerationCallback, LanguageCallback
from app.bot.database import (
    add_reason, add_user, get_chat_locale,
    delete_user_reason, delete_user_reasons,
    delete_warn, get_user_reasons, add_chat_info
)
from app.bot.utils import (
    answer_message, ban_with_message, handle_ban, handle_mute,
    handle_unban, handle_unban_for_callback, handle_unmute,
    handle_unmute_for_callback
)

admin_router: Router = Router()

@admin_router.message(Command("mute"))
async def mute_handler(
    bot: Bot,
    redis: Redis,
    i18n: I18nContext,
    message: Message, 
    command: CommandObject
) -> Message:
    chat: Chat = message.chat
    reply: Optional[Message] = message.reply_to_message
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    if not reply or not reply.from_user:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    reply_user: User = reply.from_user

    return await handle_mute(
        bot=bot,
        redis=redis,
        i18n=i18n,
        locale=locale,
        reply_user=reply_user,
        message=message, 
        command=command
    )


@admin_router.message(Command("ban"))
async def ban_handler(
    bot: Bot,
    redis: Redis,
    i18n: I18nContext,
    message: Message, 
    command: CommandObject
) -> Message:
    chat: Chat = message.chat
    reply: Optional[Message] = message.reply_to_message
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    if not reply or not reply.from_user:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    reply_user: User = reply.from_user

    return await handle_ban(
        bot=bot,
        i18n=i18n,
        locale=locale,
        reply_user=reply_user,
        message=message, 
        command=command
    )

@admin_router.callback_query(ModerationCallback.filter(F.action == "unmute"))
async def unmute_callback_handler(
    callback_query: CallbackQuery,
    redis: Redis,
    callback: ModerationCallback, 
    i18n: I18nContext,
    bot: Bot
) -> Optional[Message]:
    message: Optional[MaybeInaccessibleMessage] = callback_query.message

    if not isinstance(message, Message):
        return None
    
    chat: Chat = message.chat
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    return await handle_unmute_for_callback(
        bot=bot, 
        i18n=i18n,
        locale=locale,
        message=message,
        callback=callback,
        callback_query=callback_query
    )


@admin_router.callback_query(ModerationCallback.filter(F.action == "unban"))
async def unban_callback_handler(
    callback_query: CallbackQuery,
    redis: Redis,
    callback: ModerationCallback,
    i18n: I18nContext, 
    bot: Bot
) -> Optional[Message]:
    message: Optional[MaybeInaccessibleMessage] = callback_query.message

    if not isinstance(message, Message):
        return None

    chat: Chat = message.chat
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    return await handle_unban_for_callback(
        bot=bot, 
        i18n=i18n,
        locale=locale,
        message=message,
        callback=callback,
        callback_query=callback_query
    )


@admin_router.message(Command("unmute"))
async def unmute_handler(
    i18n: I18nContext,
    redis: Redis,
    message: Message,
    bot: Bot
) -> Message:
    chat: Chat = message.chat
    reply: Optional[Message] = message.reply_to_message
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    if not reply or not reply.from_user:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    reply_user: User = reply.from_user

    return await handle_unmute(
        bot=bot,
        redis=redis,
        i18n=i18n,
        locale=locale,
        reply_user=reply_user, 
        message=message
    )


@admin_router.message(Command("unban"))
async def unban_handler(
    i18n: I18nContext,
    redis: Redis,
    message: Message,
    bot: Bot
) -> Message:
    chat: Chat = message.chat
    reply: Optional[Message] = message.reply_to_message
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    if not reply or not reply.from_user:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    reply_user: User = reply.from_user

    return await handle_unban(
        bot=bot,
        i18n=i18n,
        reply_user=reply_user, 
        locale=locale,
        message=message
    )


@admin_router.message(Command("warn"))
async def warn_user(
    bot: Bot,
    redis: Redis,
    message: Message, 
    i18n: I18nContext,
    command: CommandObject
) -> Optional[Message]:
    chat: Chat = message.chat
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )
    error_reason: str = i18n.get(
        'error-reason', 
        locale
    )
    reason: str = command.args if command.args else error_reason
    reply: Optional[Message] = message.reply_to_message
    user: Optional[User] = message.from_user

    if not user:
        return None

    if not reply or not reply.from_user:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    reply_user: User = reply.from_user
    warns: int = await add_user(
        chat_id=chat.id,
        user_id=reply_user.id
    )

    await add_reason(
        user_id=reply_user.id, 
        chat_id=chat.id,
        reason=reason
    )

    if warns >= 3:
        await delete_warn(
            user_id=reply_user.id,
            chat_id=chat.id,
            warns=3
        )

        await delete_user_reasons(
            chat_id=chat.id,
            user_id=reply_user.id
        )

        return await ban_with_message(
            bot=bot,
            locale=locale,
            i18n=i18n,
            chat_id=chat.id,
            user_id=reply_user.id,
            button_texts=["Unban"],
            callback_datas=[
                ModerationCallback(
                    action='unban',
                    user_id=reply_user.id
                ).pack()
            ],
            message_text=i18n.get(
                'warn-ban',
                locale,
                user_id=reply_user.id,
                user_full_name=reply_user.full_name
            )
        )

    else:
        return await answer_message(
            bot=bot,
            chat_id=chat.id,
            button_texts=["Delete Warn"],
            callback_datas=[
                ModerationCallback(
                    action='rewarn',
                    user_id=reply_user.id
                ).pack()
            ],
            text=i18n.get(
                'add_warn',
                locale,
                user_id=reply_user.id,
                user_full_name=reply_user.full_name,
                admin_id=user.id,
                admin_full_name=user.full_name,
                reason=reason,
                warns=warns
            )
        )


@admin_router.callback_query(ModerationCallback.filter(F.action == "rewarn"))
async def rewarn_callback_handler(
    bot: Bot,
    redis: Redis,
    i18n: I18nContext,
    callback_query: CallbackQuery, 
    callback: ModerationCallback
) -> Optional[Message]:
    message: Optional[MaybeInaccessibleMessage] = callback_query.message

    if not isinstance(message, Message):
        return None

    await message.delete()

    chat: Chat = message.chat
    user_id: int = callback.user_id
    admin_user: User = callback_query.from_user
    user = await bot.get_chat_member(
        user_id=user_id,
        chat_id=chat.id
    )
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    await delete_warn(
        user_id=user_id,
        chat_id=chat.id,
        warns=1
    )

    await delete_user_reason(
        user_id=user_id,
        chat_id=chat.id
    )

    return await answer_message(
        bot=bot,
        delay=30,
        chat_id=chat.id,
        text=i18n.get(
            'delete_warn',
            locale,
            user_id=user.user.id,
            user_full_name=user.user.full_name,
            admin_id=admin_user.id,
            admin_full_name=admin_user.full_name
        )
    )


@admin_router.message(Command('warns'))
async def get_warns(
    message: Message,
    redis: Redis,
    i18n: I18nContext,
    bot: Bot
) -> Message:
    reply: Optional[Message] = message.reply_to_message
    chat: Chat = message.chat
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,    
        redis=redis
    )

    if not reply or not reply.from_user:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    reply_user: User = reply.from_user
    user_id: int = reply_user.id
    reasons: str = await get_user_reasons(
        chat_id=chat.id,
        locale=locale,
        i18n=i18n,
        user_id=user_id
    )

    return await answer_message(
        bot=bot, 
        chat_id=chat.id,
        text=i18n.get(
            "user-reasons",
            locale,
            user_id=user_id,
            warns_reasons=reasons,
            user_full_name=reply_user.full_name
        )
    )


@admin_router.message(Command("set_rules"))
async def help_handler(
    bot: Bot,
    redis: Redis,
    i18n: I18nContext,
    message: Message, 
    command: CommandObject
) -> Message:
    message_id: Optional[str] = command.args
    chat: Chat = message.chat
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    if not message_id or not re.fullmatch(r"\d+", message_id):
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
                "error-args",
                locale
            )
        )

    rules_id: int = int(message_id)

    await add_chat_info(
        redis=redis,
        chat_id=chat.id, 
        rules_id=rules_id
    )

    return await answer_message(
        bot=bot,
        chat_id=chat.id,
        text=i18n.get(
            "success-rules",
            locale
        )
    )


@admin_router.message(Command('set_language'))
async def set_language(
    bot: Bot,
    message: Message,
    i18n: I18nContext,
) -> Message:
    return await answer_message(
        bot=bot,
        chat_id=message.chat.id,
        buttons_level=2,
        button_texts=[
            locale 
            for locale in Locale
        ],
        callback_datas=[
            LanguageCallback(
                language=locale
            ).pack() 
            for locale in Locale
        ],
        text=i18n.get(
            "set-language"
        )
    )


@admin_router.callback_query(LanguageCallback.filter())
async def set_language_callback(
    callback_query: CallbackQuery,
    redis: Redis,
    callback_data: LanguageCallback,
    i18n: I18nContext,
    bot: Bot
) -> Optional[Message]:
    message: Optional[MaybeInaccessibleMessage] = callback_query.message

    if not isinstance(message, Message):
        return None

    await message.delete()

    chat: Chat = message.chat
    locale: Optional[str] = await get_chat_locale(
        chat_id=chat.id,
        redis=redis
    )

    await add_chat_info(
        chat_id=chat.id,
        redis=redis,
        chat_locale=callback_data.language
    )

    return await answer_message(
        bot=bot,
        chat_id=chat.id,
        text=i18n.get(
            "success-language",
            locale
        )
    )