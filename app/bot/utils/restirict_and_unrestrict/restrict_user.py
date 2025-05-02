from aiogram import Bot
from aiogram.filters import CommandObject
from fluentogram import TranslatorRunner
from aiogram.types import Chat, Message, User

from app.bot.keyboards import ModerationCallback
from ..helpers import (
    answer_message, ban_with_message, 
    mute_with_message, parse_time_and_reason
)


async def handle_mute(
    bot: Bot, 
    message: Message,
    reply_user: User, 
    command: CommandObject,
    i18n: TranslatorRunner
) -> None:
    if not message.from_user:
        await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    if not command.args:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-restrict-args'
            )
        )
        return None

    chat: Chat = message.chat
    admin_user: User = message.from_user
    until_date, reason, readable_time = parse_time_and_reason(
        args=command.args,
        i18n=i18n
    )

    await mute_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=reply_user.id,
        until_date=until_date,
        buttons_level=1,
        button_texts=['Unmute✔️'],
        callback_datas=[
            ModerationCallback(
                action='unmute',
                user_id=reply_user.id
            ).pack()
        ],
        message_text=i18n.get(
            'mute-user',
            user_id=reply_user.id,
            user_full_name=reply_user.full_name,
            measure_time=readable_time,
            reason=reason,
            admin_id=admin_user.id,
            admin_full_name=admin_user.full_name
        )
    )


async def handle_ban(
    bot: Bot, 
    message: Message,
    reply_user: User, 
    command: CommandObject,
    i18n: TranslatorRunner
) -> None:
    if not message.from_user:
        await answer_message(
            bot=bot,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    if not command.args:
        await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-restrict-args'
            )
        )
        return None

    chat: Chat = message.chat
    admin_user: User = message.from_user
    until_date, reason, readable_time = parse_time_and_reason(
        args=command.args,
        i18n=i18n
    )

    await ban_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat.id,
        user_id=reply_user.id,
        until_date=until_date,
        buttons_level=1,
        button_texts=['Unban✔️'],
        callback_datas=[
            ModerationCallback(
                action='unban',
                user_id=reply_user.id
            ).pack()
        ],
        message_text=i18n.get(
            'ban-user',
            user_id=reply_user.id,
            user_full_name=reply_user.full_name,
            measure_time=readable_time,
            reason=reason,
            admin_id=admin_user.id,
            admin_full_name=admin_user.full_name
        )
    )