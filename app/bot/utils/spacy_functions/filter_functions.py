from datetime import datetime
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, User
from fluentogram import TranslatorRunner
from spacy.language import Language
from spacy.tokens import Doc

from app.bot.keyboards import ModerationCallback
from ..helpers import answer_message, mute_with_message


async def check_message_to_https_links(
    bot: Bot,
    i18n: TranslatorRunner,
    message: Message,
    nlp_model: Language
) -> None:
    if not message.from_user:
        return None

    if not message.text:
        return None

    doc: Doc = nlp_model(message.text)  
    user: User = message.from_user
    links: List[str] = [token.text for token in doc if token.like_url]

    for link in links:
        if not link.startswith("https://"):
            try:
                await message.delete()
            except TelegramBadRequest:
                return None

            await answer_message(
                bot=bot,
                chat_id=message.chat.id,
                text=i18n.get(
                    'check-links',
                    user_id=user.id,
                    user_full_name=user.full_name
                )
            )  


async def check_message_to_bad_words(
    bot: Bot,
    i18n: TranslatorRunner,
    message: Message,
    nlp_model: Language,
    forbidden_words: List[str],
    until_date: datetime
) -> None:
    if not message.from_user:
        return None

    if not message.text:  
        return None

    user: User = message.from_user
    doc: Doc = nlp_model(message.text)  

    for token in doc:
        if token.text.lower() in forbidden_words:
            await mute_with_message(
                bot=bot,
                i18n=i18n,
                chat_id=message.chat.id,
                user_id=user.id,
                until_date=until_date,
                buttons_level=1,
                button_texts=['Unmute✔️'],
                callback_datas=[
                    ModerationCallback(
                        action='unmute',
                        user_id=user.id
                    ).pack()
                ],
                message_text=i18n.get(
                    'badwords-muting',
                    user_id=user.id,
                    user_full_name=user.full_name
                )
            )  