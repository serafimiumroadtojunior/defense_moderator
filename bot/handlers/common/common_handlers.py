from typing import Optional

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Chat, Message

from utils import answer_message

common_router: Router = Router()

@common_router.message(Command("message_id"))
async def send_message_id(message: Message) -> None:
    chat: Optional[Chat] = message.chat
    reply_to_message: Optional[Message] = message.reply_to_message

    if chat is None or message.bot is None or reply_to_message is None:
        return

    message_id: str = f"Message ID: {reply_to_message.message_id}"

    await answer_message(
        bot=message.bot, 
        chat_id=chat.id, 
        text=message_id,
        delay=30
    )

@common_router.message(Command("help"))
async def help_for_admins(message: Message) -> None:
    chat: Optional[Chat] = message.chat
    message_admin: str = (
        "/mute - Restricts the user from sending messages\n"
        "/unmute - Allows the user to send messages again\n"
        "/ban - Bans the user (excludes from the group)\n"
        "/unban - Bans the user (excludes from the group)\n"
        "/warn - Gives the user a warning\n"
        "/message_id - Returns the ID of the last replied message\n"
        "/set_rules - Assigns rules"
    )

    if chat is None or message.bot is None:
        return

    await answer_message(
        bot=message.bot, 
        chat_id=chat.id, 
        text=message_admin,
        delay=30
    )