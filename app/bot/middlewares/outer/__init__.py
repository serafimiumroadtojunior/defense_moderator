import os
from typing import List

from aiogram import Dispatcher
from dotenv import load_dotenv

from app.bot.config import ENV_FILE
from .goodbye_middleware import GoodbyeMiddleware
from .message_filter import FilterWordsMiddleware
from .welcome_middleware import WelcomeMiddleware
from .group_middleware import CheckGroupMiddleware
from .posts_tracker import ChannelPostMiddleware
from .messages_stats import StatsSpamMiddleware
from .locales_middleware import TranslatorRunnerMiddleware
from .antispam import (
    AntiSpamMiddleware, UniqueAntiSpamMiddleware,
    ReactionsAntiSpamMiddleware, PercentSpamParseMiddleware
)

load_dotenv(dotenv_path=ENV_FILE)

def setup_outer_middlewares(dispatcher: Dispatcher) -> None:
    file_path = os.getenv("FORBIDDEN_WORDS_FILE")
    if file_path is None:
        raise ValueError("FORBIDDEN_WORDS_FILE environment variable not set")

    dispatcher.message.outer_middleware(
        TranslatorRunnerMiddleware()
    )
    dispatcher.message.outer_middleware(
        CheckGroupMiddleware()
    )
    dispatcher.message.outer_middleware(
        StatsSpamMiddleware()
    )
    dispatcher.message.outer_middleware(
        ChannelPostMiddleware()
    )
    dispatcher.chat_member.outer_middleware(
        WelcomeMiddleware()
    )
    dispatcher.chat_member.outer_middleware(
        GoodbyeMiddleware()
    )
    dispatcher.message.outer_middleware(
        AntiSpamMiddleware()
    )
    dispatcher.message.outer_middleware(
        UniqueAntiSpamMiddleware()
    )
    dispatcher.message_reaction.outer_middleware(
        ReactionsAntiSpamMiddleware()
    )
    dispatcher.chat_member.outer_middleware(
        PercentSpamParseMiddleware()
    )
    dispatcher.message.outer_middleware(
        FilterWordsMiddleware(
            file_path=file_path
        )
    )


__all__: List[str] = [
    "setup_outer_middlewares"
]