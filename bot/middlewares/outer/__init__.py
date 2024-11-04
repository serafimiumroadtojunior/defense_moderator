import os
from typing import List

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from .goodbye_middleware import GoodbyeMiddleware
from .message_filter import FilterWordsMiddleware
from .welcome_middleware import WelcomeMiddleware

load_dotenv(dotenv_path=os.path.join("defense_moderator", ".env"))

def setup_outer_middlewares(dispatcher: Dispatcher, bot: Bot) -> None:
    file_path = os.getenv("FORBIDDEN_WORDS_FILE")
    if file_path is None:
        raise ValueError("FORBIDDEN_WORDS_FILE environment variable not set")

    dispatcher.message.outer_middleware(
        WelcomeMiddleware(bot=bot)
    )
    dispatcher.message.outer_middleware(
        GoodbyeMiddleware(bot=bot)
    )
    dispatcher.message.outer_middleware(
        FilterWordsMiddleware(
            bot=bot, 
            file_path=file_path
        )
    )


__all__: List[str] = [
    "setup_outer_middlewares"
]