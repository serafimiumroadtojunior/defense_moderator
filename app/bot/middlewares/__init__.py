from typing import List

from aiogram import Bot, Dispatcher

from .inner import setup_inner_middlewares
from .outer import setup_outer_middlewares


def setup_middlewares(dispatcher: Dispatcher, bot: Bot):
    setup_outer_middlewares(bot=bot, dispatcher=dispatcher)
    setup_inner_middlewares(bot=bot, dispacther=dispatcher)

__all__: List[str] = ["setup_middlewares"]