from typing import List

from redis.asyncio import Redis
from aiogram import Dispatcher, Bot

from app.bot.settings import Settings
from .goodbye_middleware import GoodbyeMiddleware
from .message_filter import FilterWordsMiddleware
from .welcome_middleware import WelcomeMiddleware
from .group_middleware import CheckGroupMiddleware
from .posts_tracker import ChannelPostMiddleware
from .messages_stats import StatsSpamMiddleware
from .antispam import (
    AntiSpamMiddleware, UniqueAntiSpamMiddleware,
    ReactionsAntiSpamMiddleware, PercentSpamParseMiddleware
)

def setup_outer_middlewares(
    dispatcher: Dispatcher,
    bot: Bot,
    redis: Redis,
    settings: Settings
) -> None:
    file_path = settings.bad_words_file

    dispatcher.message.outer_middleware(
        CheckGroupMiddleware(
)
    )
    dispatcher.message.outer_middleware(
        StatsSpamMiddleware()
    )
    dispatcher.message.outer_middleware(
        ChannelPostMiddleware(
            redis=redis
        )
    )
    dispatcher.chat_member.outer_middleware(
        WelcomeMiddleware(
            bot=bot,
            redis=redis
        )
    )
    dispatcher.chat_member.outer_middleware(
        GoodbyeMiddleware(
            bot=bot,
            redis=redis
        )
    )
    dispatcher.message.outer_middleware(
        AntiSpamMiddleware(
            bot=bot,
            redis=redis
        )
    )
    dispatcher.message.outer_middleware(
        UniqueAntiSpamMiddleware(
            bot=bot,
            redis=redis
        )
    )
    dispatcher.message_reaction.outer_middleware(
        ReactionsAntiSpamMiddleware(
            bot=bot,
            redis=redis
        )
    )
    dispatcher.chat_member.outer_middleware(
        PercentSpamParseMiddleware(
            bot=bot,
            redis=redis
        )
    )
    dispatcher.message.outer_middleware(
        FilterWordsMiddleware(
            file_path=file_path,
            bot=bot,
            redis=redis
        )
    )


__all__: List[str] = [
    "setup_outer_middlewares"
]