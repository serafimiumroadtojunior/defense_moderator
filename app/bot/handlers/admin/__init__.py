from typing import List

from aiogram import Dispatcher

from .admin_handlers import admin_router


def setup_admin_router(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(admin_router)

__all__: List[str] = [
    "setup_admin_router", 
    "admin_router"
]