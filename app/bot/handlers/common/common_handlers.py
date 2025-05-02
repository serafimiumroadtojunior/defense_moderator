from typing import Optional

from aiogram import Router, Bot
from fluentogram import TranslatorRunner
from aiogram.filters import Command
from aiogram.types import Chat, Message

from app.bot.utils import answer_message

common_router: Router = Router()

@common_router.message(Command("message_id"))
async def send_message_id(
    bot: Bot,
    i18n: TranslatorRunner,
    message: Message
) -> None:
    chat: Chat = message.chat
    reply: Optional[Message] = message.reply_to_message

    if not reply:
        await answer_message(
            bot=bot, 
            chat_id=chat.id, 
            text=i18n.get(
                'error-reply'
            )
        )
        return None

    await answer_message(
        bot=bot, 
        chat_id=chat.id, 
        text=i18n.get(
            'message-id', 
            message_id=reply.message_id
        )
    )