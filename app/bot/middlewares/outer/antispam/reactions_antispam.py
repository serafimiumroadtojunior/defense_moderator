from typing import Callable, Dict, Any, Awaitable, Optional
from datetime import timedelta, datetime

from fluentogram import TranslatorRunner
from aiogram import BaseMiddleware, Bot
from aiogram.types import (
    MessageReactionUpdated, 
    TelegramObject, Update
)

from app.bot.utils import count_reactions_spam


class ReactionsAntiSpamMiddleware(BaseMiddleware):
    def __init__(self):
        self.until_date: datetime = datetime.now() + timedelta(minutes=30)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        if event.message_reaction:
            reaction: MessageReactionUpdated = event.message_reaction
            bot: Optional[Bot] = data.get('bot')
            i18n: Optional[TranslatorRunner] = data.get('i18n')

            if not bot or not i18n:
                return await handler(event, data)

            if reaction.new_reaction:
                await count_reactions_spam(
                    bot=bot,
                    i18n=i18n,
                    until_date=self.until_date,
                    reactions=reaction,
                    count_spam=3
                )

            return await handler(event, data)
        return await handler(event, data)