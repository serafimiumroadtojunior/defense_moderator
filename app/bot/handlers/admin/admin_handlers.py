import re
from typing import List, Optional, Union

from aiogram import Bot, F, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import (
    CallbackQuery, Chat, 
    Message, User
)

from app.bot.database import (
    add_reason, add_rules_id, add_user, add_warn,
    delete_user_reason, delete_user_reasons,
    delete_warn, get_user_reasons, reset_warns
)
from app.bot.utils import (
    answer_message, ban_with_message, handle_ban, handle_mute,
    handle_unban, handle_unban_for_callback, handle_unmute,
    handle_unmute_for_callback
)

admin_router: Router = Router()

@admin_router.message(Command("mute"))
async def mute_handler(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot
    if not bot:
        return

    await handle_mute(
        bot=bot,
        message=message, 
        command=command
    )


@admin_router.message(Command("ban"))
async def ban_handler(message: Message, command: CommandObject) -> None:
    bot: Optional[Bot] = message.bot
    if not bot:
        return

    await handle_ban(
        bot=bot, 
        message=message, 
        command=command
    )


@admin_router.callback_query(F.data.startswith("unmute_"))
async def unmute_callback_handler(callback_query: CallbackQuery) -> None:
    if not isinstance(callback_query.message, Message):
        return

    bot: Optional[Bot] = callback_query.bot
    if not bot:
        return

    await handle_unmute_for_callback(
        bot=bot, 
        callback_query=callback_query
    )


@admin_router.callback_query(F.data.startswith("unban_"))
async def unban_callback_handler(callback_query: CallbackQuery) -> None:
    if not isinstance(callback_query.message, Message):
        return

    bot: Optional[Bot] = callback_query.bot
    if not bot:
        return

    await handle_unban_for_callback(
        bot=bot, 
        callback_query=callback_query
    )


@admin_router.message(Command("unmute"))
async def unmute_handler(message: Message) -> None:
    bot: Optional[Bot] = message.bot
    if not bot:
        return

    await handle_unmute(
        bot=bot, 
        message=message
    )


@admin_router.message(Command("unban"))
async def unban_handler(message: Message) -> None:
    bot: Optional[Bot] = message.bot
    if not bot:
        return

    await handle_unban(
        bot=bot, 
        message=message
    )


@admin_router.message(Command("warn"))
async def warn_user(message: Message, command: CommandObject) -> None:
    chat: Optional[Chat] = message.chat
    reply: Optional[Message] = message.reply_to_message

    if not reply or not reply.from_user:
        return
    
    if not chat or not message.bot:
        return
    
    reason: str = command.args if command.args else "no reason provided"
    user_id: int = reply.from_user.id
    bot: Bot = message.bot

    await add_user(
        chat_id=chat.id,
        user_id=user_id
    )

    await add_reason(
        user_id=user_id, 
        chat_id=chat.id,
        reason=reason
    )

    warns: int = await add_warn(
        user_id=user_id,
        chat_id=chat.id
    )

    if warns >= 3:
        await reset_warns(
            chat_id=chat.id,
            user_id=user_id
        )

        await delete_user_reasons(
            chat_id=chat.id,
            user_id=user_id
        )

        await ban_with_message(
            bot=bot,
            chat_id=chat.id,
            user_id=user_id,
            message_text=(
                f"👀<a href='tg://user?id={user_id}'><b>{reply.from_user.first_name}</b></a>" 
                "has been permanently banned for receiving 3 warnings."
            )
        )
        
    else:
        await answer_message(
            bot=bot,
            chat_id=chat.id,
            delay=30,
            callback_data=f"rewarn_{user_id}",
            button_text="Delete Warn✅",
            text=(
                f"👀<a href='tg://user?id={user_id}'><b>{reply.from_user.first_name}</b></a>" 
                "has received a warning for: {reason}."
                "\n<i>Current count: {warns}.</i>"
            )
        )


@admin_router.callback_query(F.data.startswith("rewarn_"))
async def rewarn_callback_handler(callback_query: CallbackQuery) -> None:
    if not isinstance(callback_query.message, Message):
        return
    
    if not callback_query.data or not callback_query.bot:
        return
    
    await callback_query.message.delete()

    bot: Bot = callback_query.bot
    chat: Chat = callback_query.message.chat
    user_id_str: Optional[str] = callback_query.data.split("_")[1]

    if user_id_str is not None and callback_query.from_user is not None:
        user_id: int = int(user_id_str)
        user: User = callback_query.from_user

        await delete_warn(
            user_id=user_id,
            chat_id=chat.id
        )

        await delete_user_reason(
            user_id=user_id,
            chat_id=chat.id
        )

        await answer_message(
            bot=bot,
            delay=30,
            chat_id=chat.id,
            text=(
                f"👀The <a href='tg://user?id={user.id}'><b>{user.first_name}</b></a>'s"
                "warn has been removed"
            )
        )


@admin_router.message(Command('warns'))
async def get_warns(message: Message) -> None:
    reply: Optional[Message] = message.reply_to_message

    if not message.chat or not message.bot:
        return
    
    if not reply or not reply.from_user:
        return

    user_id: int = reply.from_user.id
    reasons: Union[List[str], str] = await get_user_reasons(
        chat_id=message.chat.id,
        user_id=user_id
    )

    await answer_message(
        delay=30,
        bot=message.bot, 
        chat_id=message.chat.id,
        text=(
            "🛑Warns for user" 
            f"<a href='tg://user?id={user_id}'>{reply.from_user.first_name}</a>: \n{reasons}"
        )
    )


@admin_router.message(Command("set_rules"))
async def help_handler(message: Message, command: CommandObject) -> None:
    message_id: Optional[str] = command.args
    chat: Optional[Chat] = message.chat
    bot: Optional[Bot] = message.bot
    
    if not chat or not bot:
        return

    if not message_id or not re.fullmatch(r"\d+", message_id):
        await answer_message(
            bot=bot,
            chat_id=chat.id,
            text="🔴Error: Please provide a valid message ID containing only digits."
        )
        return

    message_id_int: int = int(message_id)

    await add_rules_id(
        chat_id=chat.id, 
        message_id=message_id_int
    )

    await answer_message(
        bot=bot,
        chat_id=chat.id,
        text="👀<b>Success!</b> Rules have been successfully added!",
        delay=30
    )