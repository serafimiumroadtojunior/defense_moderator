from typing import List

from aiogram import Dispatcher

from .inner import setup_inner_middlewares
from .outer import setup_outer_middlewares


def setup_middlewares(dispatcher: Dispatcher):
    setup_outer_middlewares(dispatcher=dispatcher)
    setup_inner_middlewares(dispacther=dispatcher)

__all__: List[str] = ["setup_middlewares"]