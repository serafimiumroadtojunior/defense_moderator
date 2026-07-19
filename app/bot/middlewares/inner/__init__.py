from typing import List

from redis.asyncio.client import Redis
from aiogram import Dispatcher, Bot

from app.bot.handlers.admin import admin_router
from app.bot.handlers.user import user_router
from .anti_flood import AntiFloodMiddleware
from .callback_filter import CallbackFilterMiddleware
from .admin_checker import (
    AdminCheckerMiddleware,
    CallbackAdminCheckerMiddleware
)


def setup_inner_middlewares(
    bot: Bot, 
    redis: Redis,
    dispacther: Dispatcher
) -> None:
    admin_router.message.middleware(
        AdminCheckerMiddleware(
            bot=bot,
            redis=redis
        )
    )
    admin_router.callback_query.middleware(
        CallbackAdminCheckerMiddleware(
            bot=bot,
            redis=redis
        )
    )
    user_router.callback_query.middleware(
        CallbackFilterMiddleware(
            redis=redis
        )
    )
    dispacther.message.middleware(
        AntiFloodMiddleware()
    )

__all__: List[str] = [
    "setup_inner_middlewares"
]