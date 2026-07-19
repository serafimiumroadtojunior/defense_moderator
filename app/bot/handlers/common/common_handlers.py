from typing import Optional

from redis.asyncio.client import Redis
from aiogram_i18n import I18nContext
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import  Chat, Message

from app.bot.database import get_chat_locale
from app.bot.utils import answer_message

common_router: Router = Router()

@common_router.message(Command("message_id"))
async def send_message_id(
    bot: Bot,
    redis: Redis,
    i18n: I18nContext,
    message: Message
) -> Message:
    chat: Chat = message.chat
    reply: Optional[Message] = message.reply_to_message
    locale: Optional[str] = await get_chat_locale(
        redis=redis, 
        chat_id=chat.id
    )

    if not reply:
        return await answer_message(
            bot=bot, 
            chat_id=chat.id, 
            text=i18n.get(
                'error-reply',
                locale
            )
        )

    return await answer_message(
        bot=bot, 
        chat_id=chat.id, 
        text=i18n.get(
            'message-id', 
            locale,
            message_id=reply.message_id
        )
    )