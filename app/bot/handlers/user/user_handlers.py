from typing import Optional
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message, User
from aiogram.filters import Command, CommandObject

from app.bot.database import get_mute_flag
from app.bot.utils import (
    unmute_with_message, mute_with_message,
    ModerationCallback, report_user
)

user_router: Router = Router()

@user_router.callback_query(ModerationCallback.filter(F.action == 'captcha'))
async def captcha_complete(callback_query: CallbackQuery) -> None:
    if not isinstance(callback_query.message, Message):
        return

    if not callback_query.message.chat or not callback_query.message.bot:
        return

    await callback_query.message.delete()

    user: User = callback_query.from_user
    bot: Bot = callback_query.message.bot
    chat_id: int = callback_query.message.chat.id
    mute_flag: Optional[datetime] = await get_mute_flag()

    if not mute_flag:
        await unmute_with_message(
            bot=bot,
            chat_id=chat_id,
            user_id=user.id,
            message_text=(
                f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
                "has completed CAPTCHA!"
            )
        )

    await mute_with_message(
        bot=bot,
        chat_id=chat_id,
        user_id=user.id,
        until_date=mute_flag,
        action='mute',
        message_text=(
            f"<a href='tg://user?id={user.id}'>{user.full_name}</a>"
            "has been muted \nfor the reason: Attempted abuse of the CAPTCHA system."
        )
    )


@user_router.message(Command('report'))
async def report_command(
    message: Message, 
    command: CommandObject
) -> None:
    bot: Optional[Bot] = message.bot
    if not bot:
        return

    await report_user(
        message=message,
        command=command,
        bot=bot
    )