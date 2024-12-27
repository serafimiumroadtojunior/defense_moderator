from datetime import datetime
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, User
from spacy.language import Language
from spacy.tokens import Doc

from ..helpers import answer_message, mute_with_message


async def check_message_to_https_links(
    bot: Bot,
    message: Message,
    nlp_model: Language
) -> None:
    if not message.chat or not message.from_user:
        return

    if not message.text:
        return

    doc: Doc = nlp_model(message.text)  
    user: User = message.from_user
    links: List[str] = [token.text for token in doc if token.like_url]

    for link in links:
        if not link.startswith("https://"):
            try:
                await message.delete()
            except TelegramBadRequest:
                return

            await answer_message(
                bot=bot,
                delay=30,
                chat_id=message.chat.id,
                text=(
                    '🔴Only HTTPS links are allowed'
                    f'<a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
                )
            )
            return  


async def check_message_to_bad_words(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    forbidden_words: List[str],
    until_date: datetime
) -> None:
    if not message.chat or not message.from_user:
        return

    if not message.text:  
        return

    user: User = message.from_user
    doc: Doc = nlp_model(message.text)  

    for token in doc:
        if token.text.lower() in forbidden_words:
            await mute_with_message(
                bot=bot,
                chat_id=message.chat.id,
                user_id=user.id,
                until_date=until_date,
                action='unmute',
                message_text=(
                    f'<a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
                    'has been muted \nfor the reason: Profanity.'
                )
            )
            return  