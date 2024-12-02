from typing import List, Optional

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from app.bot.utils import unmute_with_message

user_router: Router = Router()

@user_router.callback_query(F.data.startswith('captcha'))
async def captcha_complete(callback_query: CallbackQuery) -> None:
    if not isinstance(callback_query.message, Message):
        return

    if not callback_query.message.chat or not callback_query.data:
        return

    await callback_query.message.delete()
    
    data_parts: List[str] = callback_query.data.split('_')
    user_id: int = int(data_parts[1])
    bot: Optional[Bot] = callback_query.message.bot
    chat_id: int = callback_query.message.chat.id

    if not bot:
        return

    await unmute_with_message(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        message_text=(
            f"<a href='tg://user?id={user_id}'>{callback_query.from_user.first_name}</a>"
            "has completed CAPTCHA!"
        )
    )