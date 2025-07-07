import asyncio
from contextlib import suppress
from datetime import datetime
from typing import Optional, Sequence

from aiogram import Bot
from aiogram_i18n import I18nContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    ChatMemberMember, Message,
    ResultChatMemberUnion
)

from app.bot.keyboards import customed_keyboard


async def send_unrestriction_message(
    bot: Bot, 
    chat_id: int,
    user_id: int,
    i18n: I18nContext,
    locale: Optional[str], 
    new_datetime: Optional[datetime]
) -> Optional[Message]:
    if not new_datetime:
        return None

    wait_time: float = (new_datetime - datetime.now()).total_seconds()
    chat_member: ResultChatMemberUnion = await bot.get_chat_member(
        chat_id=chat_id, 
        user_id=user_id
    )

    if wait_time <= 0:
        return await answer_message(
            bot=bot,
            chat_id=chat_id,
            delay=10,
            text=i18n.get(
               'error-time',
               locale 
            )
        )

    await asyncio.sleep(wait_time)

    if isinstance(chat_member, ChatMemberMember):
        return await answer_message(
            bot=bot,
            chat_id=chat_id,
            text=i18n.get(
                'unterestrict-message',
                locale,
                user_id=user_id,
                user_full_name=chat_member.user.full_name,
            )
        )
    
    return None


async def answer_message(
    bot: Bot,
    chat_id: int,
    text: str,
    delay: int = 30,
    flag: bool = False,
    button_texts: Optional[Sequence[str]] = None,
    callback_datas: Optional[Sequence[str]] = None,
    buttons_level: Optional[int] = None
) -> Message:
    response_message: Message = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=await customed_keyboard(
            buttons_text=button_texts,
            callback_data=callback_datas,
            buttons_level=buttons_level
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


async def delayed_delete(
    delay: int, 
    message: Message
) -> None:
    with suppress(TelegramBadRequest, AttributeError):
        await asyncio.sleep(delay)
        await message.delete()