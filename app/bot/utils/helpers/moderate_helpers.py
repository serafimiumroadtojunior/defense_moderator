import re
from datetime import datetime, timedelta
from typing import (
    Optional, Tuple, 
    Union, List
)

from aiogram import Bot
from aiogram.filters import CommandObject
from aiogram_i18n import I18nContext
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.types import (
    ChatMemberAdministrator, 
    ChatMemberOwner, Message, User, Chat
)

from .message_functions import answer_message
from app.bot.database import add_report_flag


def parse_time_and_reason(
    args: str,
    locale: Optional[str],
    i18n: I18nContext
) -> Union[Tuple[datetime, str, str], Tuple[None, None, None]]:
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

    match unit:
        case "m":
            time_delta: timedelta = timedelta(minutes=value)
            readable_time: str = i18n.get('minutes', locale, count=value)
        case "h":
            time_delta = timedelta(hours=value)
            readable_time: str = i18n.get('hours', locale, count=value)
        case "d":
            time_delta = timedelta(days=value)
            readable_time: str = i18n.get('days', locale, count=value)
        case "w":
            time_delta = timedelta(weeks=value)
            readable_time: str = i18n.get('weeks', locale, count=value)
        case _:
            return None, None, None

    until_date: datetime = current_datetime + time_delta
    if not reason:
        reason: str = i18n.get('error-reason', locale)
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
    locale: Optional[str],
    message: Message,
    reply: Message,
    reply_user: User,
    i18n: I18nContext,
    command: CommandObject,
    bot: Bot
) -> Optional[Message]:
    error_reason: str = i18n.get(
        'error-reason', 
        locale
    )
    reason: str = command.args if command.args else error_reason
    chat: Chat = message.chat
    report: bool = await add_report_flag(
        user_id=reply_user.id,
        chat_id=chat.id
    )
    admins = await bot.get_chat_administrators(
        chat_id=chat.id
    )

    if not report:
        return await answer_message(
            bot=bot,
            delay=10,
            chat_id=message.chat.id,
            text=i18n.get(
                'error-report',
                locale
            )
        )

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
                text=i18n.get(
                    'report-user',
                    locale,
                    user_id=reply_user.id,
                    user_full_name=reply_user.full_name,
                    chat_id=chat.id,
                    chat_full_name=chat.full_name,
                    rules_id=reply.message_id,
                    reason=reason
                )
            )

        except TelegramForbiddenError:
            pass

    return None