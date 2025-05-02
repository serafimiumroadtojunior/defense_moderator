import re
from typing import Optional, Union

from aiogram import Bot, F, Router
from fluentogram import TranslatorRunner
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    CallbackQuery, Chat, 
    Message, User, InaccessibleMessage
)

from app.bot.config import Locale
from app.bot.keyboards import ModerationCallback, LanguageCallback
from app.bot.database import (
    add_reason, add_rules_id, add_user,
    delete_user_reason, delete_user_reasons,
    delete_warn, get_user_reasons, add_chat_info,
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
    i18n: TranslatorRunner,
    message: Message, 
    command: CommandObject
) -> None:
    reply: Optional[Message] = message.reply_to_message

    if not reply or not reply.from_user:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    reply_user: User = reply.from_user


    await handle_mute(
        bot=bot,
        i18n=i18n,
        reply_user=reply_user,
        message=message, 
        command=command
    )


@admin_router.message(Command("ban"))
async def ban_handler(
    bot: Bot,
    i18n: TranslatorRunner,
    message: Message, 
    command: CommandObject
) -> None:
    reply: Optional[Message] = message.reply_to_message

    if not reply or not reply.from_user:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    reply_user: User = reply.from_user

    await handle_ban(
        bot=bot,
        i18n=i18n,
        reply_user=reply_user,
        message=message, 
        command=command
    )

@admin_router.callback_query(ModerationCallback.filter(F.action == "unmute"))
async def unmute_callback_handler(
    callback_query: CallbackQuery,
    callback: ModerationCallback, 
    i18n: TranslatorRunner,
    bot: Bot
) -> None:
    message: Optional[Union[Message, InaccessibleMessage]] = callback_query.message

    if isinstance(message, InaccessibleMessage) or not message:
        return None

    await handle_unmute_for_callback(
        bot=bot, 
        i18n=i18n,
        message=message,
        callback=callback,
        callback_query=callback_query
    )


@admin_router.callback_query(ModerationCallback.filter(F.action == "unban"))
async def unban_callback_handler(
    callback_query: CallbackQuery,
    callback: ModerationCallback,
    i18n: TranslatorRunner, 
    bot: Bot
) -> None:
    message: Optional[Union[Message, InaccessibleMessage]] = callback_query.message

    if isinstance(message, InaccessibleMessage) or not message:
        return None

    await handle_unban_for_callback(
        bot=bot, 
        i18n=i18n,
        message=message,
        callback=callback,
        callback_query=callback_query
    )


@admin_router.message(Command("unmute"))
async def unmute_handler(
    i18n: TranslatorRunner,
    message: Message,
    bot: Bot
) -> None:
    reply: Optional[Message] = message.reply_to_message

    if not reply or not reply.from_user:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    reply_user: User = reply.from_user

    await handle_unmute(
        bot=bot,
        i18n=i18n,
        reply_user=reply_user, 
        message=message
    )


@admin_router.message(Command("unban"))
async def unban_handler(
    i18n: TranslatorRunner,
    message: Message,
    bot: Bot
) -> None:
    reply: Optional[Message] = message.reply_to_message

    if not reply or not reply.from_user:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    reply_user: User = reply.from_user

    await handle_unban(
        bot=bot,
        i18n=i18n,
        reply_user=reply_user, 
        message=message
    )


@admin_router.message(Command("warn"))
async def warn_user(
    bot: Bot,
    message: Message, 
    i18n: TranslatorRunner,
    command: CommandObject
) -> None:
    chat: Chat = message.chat
    reason: str = command.args if command.args else i18n.get("error-reason")
    reply: Optional[Message] = message.reply_to_message
    user: Optional[User] = message.from_user

    if not user:
        return None

    if not reply or not reply.from_user:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

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

        await ban_with_message(
            bot=bot,
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
                user_id=reply_user.id,
                user_full_name=reply_user.full_name
            )
        )

    else:
        await answer_message(
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
    i18n: TranslatorRunner,
    callback_query: CallbackQuery, 
    callback: ModerationCallback
) -> None:
    message: Optional[Union[Message, InaccessibleMessage]] = callback_query.message

    if isinstance(message, InaccessibleMessage) or not message:
        return None

    await message.delete()

    chat: Chat = message.chat
    user_id: int = callback.user_id
    admin_user: User = callback_query.from_user
    user = await bot.get_chat_member(
        user_id=user_id,
        chat_id=chat.id
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

    await answer_message(
        bot=bot,
        delay=30,
        chat_id=chat.id,
        text=i18n.get(
            'delete_warn',
            user_id=user.user.id,
            user_full_name=user.user.full_name,
            admin_id=admin_user.id,
            admin_full_name=admin_user.full_name
        )
    )


@admin_router.message(Command('warns'))
async def get_warns(
    message: Message,
    i18n: TranslatorRunner,
    bot: Bot
) -> None:
    reply: Optional[Message] = message.reply_to_message
    chat: Chat = message.chat

    if not reply or not reply.from_user:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    reply_user: User = reply.from_user
    user_id: int = reply_user.id
    reasons: str = await get_user_reasons(
        chat_id=chat.id,
        i18n=i18n,
        user_id=user_id
    )

    await answer_message(
        bot=bot, 
        chat_id=chat.id,
        text=i18n.get(
            "user-reasons",
            user_id=user_id,
            warns_reasons=reasons,
            user_full_name=reply_user.full_name
        )
    )


@admin_router.message(Command("set_rules"))
async def help_handler(
    bot: Bot,
    i18n: TranslatorRunner,
    message: Message, 
    command: CommandObject
) -> None:
    message_id: Optional[str] = command.args
    chat: Chat = message.chat

    if not message_id or not re.fullmatch(r"\d+", message_id):
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=chat.id,
            text=i18n.get(
            "error-args"
            )
        )
        return None

    message_id_int: int = int(message_id)

    await add_rules_id(
        chat_id=chat.id, 
        message_id=message_id_int
    )

    await answer_message(
        bot=bot,
        chat_id=chat.id,
        text=i18n.get(
            "success-rules",
        )
    )


@admin_router.message(Command('set_language'))
async def set_language(
    bot: Bot,
    message: Message,
    i18n: TranslatorRunner,
) -> None:
    await answer_message(
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
    callback_data: LanguageCallback,
    i18n: TranslatorRunner,
    bot: Bot
) -> None:
    message: Optional[Union[Message, InaccessibleMessage]] = callback_query.message

    if isinstance(message, InaccessibleMessage) or not message:
        return None
    
    await message.delete()

    await add_chat_info(
        chat_id=message.chat.id,
        chat_locale=callback_data.language
    )

    await answer_message(
        bot=bot,
        chat_id=message.chat.id,
        text=i18n.get(
            "success-language"
        )
    )