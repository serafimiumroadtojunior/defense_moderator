from typing import List

from aiogram import Dispatcher

from .user_handlers import user_router


def setup_user_router(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(user_router)

__all__: List[str] = [
    "setup_user_router",
    "user_router"
]