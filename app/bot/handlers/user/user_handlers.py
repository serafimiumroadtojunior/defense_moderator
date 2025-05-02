from typing import Optional
from datetime import datetime

from aiogram import Bot, F, Router
from fluentogram import TranslatorRunner
from aiogram.types import CallbackQuery, Message, User
from aiogram.filters import Command, CommandObject

from app.bot.keyboards import ModerationCallback
from app.bot.database import get_mute_flag
from app.bot.utils import (
    unmute_with_message, mute_with_message,
    report_user, answer_message
)

user_router: Router = Router()

@user_router.callback_query(ModerationCallback.filter(F.action == 'captcha'))
async def captcha_complete(
    callback_query: CallbackQuery,
    i18n: TranslatorRunner,
    bot: Bot
) -> None:
    if not isinstance(callback_query.message, Message):
        return None

    await callback_query.message.delete()

    user: User = callback_query.from_user
    chat_id: int = callback_query.message.chat.id
    mute_flag: Optional[datetime] = await get_mute_flag(
        user_id=user.id,
        chat_id=chat_id
    )

    if not mute_flag:
        await unmute_with_message(
            bot=bot,
            i18n=i18n,
            chat_id=chat_id,
            user_id=user.id,
            message_text=i18n.get(
                'complete-captcha',
                user_id=user.id,
                user_full_name=user.full_name
            )
        )

    await mute_with_message(
        bot=bot,
        i18n=i18n,
        chat_id=chat_id,
        user_id=user.id,
        until_date=mute_flag,
        buttons_level=1,
        button_texts=[
            i18n.get(
                'unmute-button'
            )
        ],
        callback_datas=[
            ModerationCallback(
                action='unmute',
                user_id=user.id
            ).pack()
        ],
        message_text=i18n.get(
            'abuse-welcome',
            user_id=user.id,
            user_full_name=user.full_name
        )
    )


@user_router.message(Command('report'))
async def report_command(
    bot: Bot,
    message: Message, 
    i18n: TranslatorRunner,
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

    await report_user(
        message=message,
        reply=reply,
        reply_user=reply_user,
        command=command,
        i18n=i18n,
        bot=bot
    )