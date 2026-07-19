from typing import List

from aiogram import Dispatcher

from .common_handlers import common_router


def setup_common_router(dispatcher: Dispatcher) -> None:
    dispatcher.include_router(common_router)

__all__: List[str] = ["setup_common_router"]