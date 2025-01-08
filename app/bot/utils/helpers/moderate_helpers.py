import re
from datetime import datetime, timedelta
from typing import (
    Optional, Tuple, 
    Union, List
)

from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import (
    ChatMemberAdministrator, 
    ChatMemberOwner, Message, User, Chat
)

from .message_functions import answer_message
from app.bot.database import add_report_flag


def parse_time_and_reason(args: str) -> Union[Tuple[datetime, str, str], Tuple[None, None, None]]:
    if not args:
        return None, None, None
    
    match: Optional[re.Match] = re.match(r"(\d+\s*[mhdw])\s*(.*)", args.lower().strip())
    if not match:
        return None, None, None

    time_string: str = match.group(1).strip()
    reason: str = match.group(2).strip()

    match = re.match(r"(\d+)\s*([mhdw])", time_string)
    if not match:
        return None, None, None

    value, unit = int(match.group(1)), match.group(2)
    current_datetime = datetime.now()

    if unit == "m":
        time_delta: timedelta = timedelta(minutes=value)
        readable_time: str = f"{value} minute{'s' if value > 1 else ''}"
    elif unit == "h":
        time_delta = timedelta(hours=value)
        readable_time = f"{value} hour{'s' if value > 1 else ''}"
    elif unit == "d":
        time_delta = timedelta(days=value)
        readable_time = f"{value} day{'s' if value > 1 else ''}"
    elif unit == "w":
        time_delta = timedelta(weeks=value)
        readable_time = f"{value} week{'s' if value > 1 else ''}"
    else:
        return None, None, None

    until_date: datetime = current_datetime + time_delta
    if not reason:
        reason = "no reason provided"
    return until_date, reason, readable_time


async def check_admin(
    bot: Bot, 
    chat_id: int, 
    user_id: int
) -> bool:
    try:
        member = await bot.get_chat_member(
            chat_id=chat_id, 
            user_id=user_id
        )

        return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner)) 
    except TelegramBadRequest:
        return False


async def report_user(
    message: Message,
    command: CommandObject,
    bot: Bot
) -> None:
    if not message.reply_to_message or not message.chat:
        return

    if not message.reply_to_message.from_user:
        return

    reason: str = command.args if command.args else 'no reason provided'
    reply: Message = message.reply_to_message
    user: User = reply.from_user
    chat: Chat = message.chat

    report: bool = await add_report_flag(
        user_id=user.id,
        chat_id=chat.id
    )

    admins = await bot.get_chat_administrators(
        chat_id=chat.id
    )

    if not report:
        return

    admins_id: List[int] = [
        admin.user.id for admin in admins
        if isinstance(admin, (ChatMemberAdministrator, ChatMemberOwner))
        and not admin.user.is_bot    
    ]

    for admin_id in admins_id:
        try:
            await answer_message(
                bot=bot,
                flag=False,
                chat_id=admin_id,
                text = (
                    f"<a href='tg://user?id={user.id}'>{user.full_name}</a>\n"
                    "<b>has been reported in chat:</b> "
                    f"<a href='https://t.me/{chat.id}'>{chat.full_name}</a>\n\n"
                    "<b>Reported message:</b> "
                    f"<a href='https://t.me/{chat.id}/{reply.message_id}'>message</a>\n"
                    f"<b>Reason:</b> {reason}"
                )
            )

        except TelegramForbiddenError:
            pass