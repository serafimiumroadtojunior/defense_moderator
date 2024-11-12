from typing import List

from aiogram import Bot, Dispatcher
from handlers.admin import admin_router
from handlers.user import user_router

from .admin_checker import (AdminCheckerMiddleware,
                            CallbackAdminCheckerMiddleware)
from .anti_flood import AntiFloodMiddleware
from .callback_filter import CallbackFilterMiddleware


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

__all__: List[str] = ["setup_inner_middlewares"]