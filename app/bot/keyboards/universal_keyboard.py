from typing import Optional, Sequence

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def customed_keyboard(
    buttons_text: Optional[Sequence[str]] = None,
    callback_data: Optional[Sequence[str]] = None,
    buttons_level: Optional[int] = None,
    pay: Optional[bool] = None
) -> Optional[InlineKeyboardMarkup]:
    if not buttons_text or not callback_data or not buttons_level:
        return None
    
    if len(buttons_text) != len(callback_data):
        return None
    
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    
    for text, data in zip(buttons_text, callback_data):
        button: InlineKeyboardButton = InlineKeyboardButton(
            text=text,
            pay=pay,
            callback_data=data
        )

        keyboard.add(button)
    keyboard.adjust(buttons_level)

    return keyboard.as_markup()