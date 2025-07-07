from typing import List

from redis.asyncio.client import Redis
from aiogram import Dispatcher, Bot

from app.bot.settings import Settings
from .inner import setup_inner_middlewares
from .outer import setup_outer_middlewares


def setup_middlewares(
    dispatcher: Dispatcher,
    settings: Settings,
    redis: Redis,
    bot: Bot
) -> None:
    setup_outer_middlewares(
        dispatcher=dispatcher,
        redis=redis,
        settings=settings,
        bot=bot
    )
    setup_inner_middlewares(
        dispacther=dispatcher,
        redis=redis,
        bot=bot
    )

__all__: List[str] = ["setup_middlewares"]