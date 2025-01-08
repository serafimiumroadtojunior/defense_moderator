import asyncio
from contextlib import suppress
from datetime import datetime
from typing import Optional

from aiogram import Bot
from aiogram.filters.callback_data import CallbackData
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    ChatMemberMember, InlineKeyboardButton,
    InlineKeyboardMarkup, Message
)


class ModerationCallback(CallbackData, prefix='moderation'):
    action: str
    user_id: int


async def send_unrestriction_message(
    bot: Bot, 
    chat_id: int,
    user_id: int, 
    new_datetime: Optional[datetime]
) -> None:
    if not new_datetime:
        return

    wait_time: float = (new_datetime - datetime.now()).total_seconds()
    chat_member = await bot.get_chat_member(
        chat_id=chat_id, 
        user_id=user_id
    )

    if wait_time <= 0:
        await answer_message(
            bot=bot,
            chat_id=chat_id,
            text="🔴Error! Time less than zero"
        )
        return

    await asyncio.sleep(wait_time)

    if isinstance(chat_member, ChatMemberMember):
        await answer_message(
            bot=bot,
            chat_id=chat_id,
            text=f'<a href="tg://user?id={chat_member.user.id}"><b>👀{chat_member.user.full_name}</b></a> has been unmuted',
            delay=30
        )


async def answer_message(
    bot: Bot,
    chat_id: int,
    text: str,
    delay: int = 10,
    flag: bool = True,
    button_text: Optional[str] = None,
    action: Optional[str] = None,
    user_id: Optional[int] = None
) -> Message:
    response_message: Message = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=await optional_keyboard(
            text=button_text,
            action=action,
            user_id=user_id
        )
    )

    if flag:
        asyncio.create_task(
            delayed_delete(
                message=response_message,
                delay=delay
            )
        )

        return response_message
    return response_message


async def optional_keyboard(
    text: Optional[str] = None,
    action: Optional[str] = None,
    user_id: Optional[int] = None
) -> Optional[InlineKeyboardMarkup]:
    if not text:
        return None

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=text,
            callback_data=ModerationCallback(
                action=action,
                user_id=user_id).pack()
        )]]
    )

    return keyboard


async def delayed_delete(
    delay: int, 
    message: Message
) -> None:
    with suppress(TelegramBadRequest, AttributeError):
        await asyncio.sleep(delay)
        await message.delete()