from typing import Callable, Dict, Any, Awaitable
from datetime import timedelta, datetime

from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    MessageReactionUpdated, 
    TelegramObject
)

from app.bot.utils import count_reactions_spam


class ReactionsAntiSpamMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.until_date: datetime = datetime.now() + timedelta(minutes=30)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, MessageReactionUpdated):
            if event.new_reaction:
                await count_reactions_spam(
                    bot=self.bot,
                    until_date=self.until_date,
                    reactions=event,
                    count_spam=3
                )

            return await handler(event, data)
        return await handler(event, data)