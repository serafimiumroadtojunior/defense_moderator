from typing import List

from aiogram import Bot, Dispatcher

from app.bot.handlers.admin import admin_router
from app.bot.handlers.user import user_router

from .anti_flood import AntiFloodMiddleware
from .callback_filter import CallbackFilterMiddleware
from .admin_checker import (
    AdminCheckerMiddleware,
    CallbackAdminCheckerMiddleware
)


def setup_inner_middlewares(dispacther: Dispatcher, bot: Bot):
    admin_router.message.middleware(
        AdminCheckerMiddleware(bot=bot)
    )
    admin_router.callback_query.middleware(
        CallbackAdminCheckerMiddleware(bot=bot)
    )
    user_router.callback_query.middleware(
        CallbackFilterMiddleware()
    )
    dispacther.message.middleware(
        AntiFloodMiddleware()
    )

__all__: List[str] = [
    "setup_inner_middlewares"
]