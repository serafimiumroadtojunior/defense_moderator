from typing import List

from aiogram import Dispatcher

from .admin import setup_admin_router
from .common import setup_common_router
from .user import setup_user_router


def setup_routers(dispatcher: Dispatcher) -> None:
    setup_admin_router(dispatcher=dispatcher)
    setup_user_router(dispatcher=dispatcher)
    setup_common_router(dispatcher=dispatcher)

__all__: List[str] = ["setup_routers"]