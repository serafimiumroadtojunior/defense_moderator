from collections import Counter
from datetime import datetime
from typing import List, Optional

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from database import get_count_messages, get_old_message
from spacy.language import Language
from spacy.tokens import Doc

from ..helpers import answer_message, mute_with_message


async def check_message_to_https_links(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    https_message: str
    ) -> None:
    if message.chat and message.from_user is None:
        return

    if message.text is None:
        return

    doc: Doc = nlp_model(message.text)  
    links: List[str] = [token.text for token in doc if token.like_url]

    for link in links:
        if not link.startswith("https://"):
            try:
                await message.delete()
            except TelegramBadRequest:
                await answer_message(
                    bot=bot,
                    chat_id=message.chat.id,
                    text="🔴Error deleting message!"
                )
                return

            if message.from_user: 
                await answer_message(
                    bot=bot,
                    chat_id=message.chat.id,
                    text=https_message.format(username=message.from_user.first_name),
                    delay=30
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

    if message.text is None:  
        return
    
    doc: Doc = nlp_model(message.text)  
    user_id: int = message.from_user.id

    for token in doc:
        if token.text.lower() in forbidden_words:
            await mute_with_message(
                bot=bot,
                chat_id=message.chat.id,
                user_id=user_id,
                until_date=until_date,
                message_text=f"<a href='tg://user?id={user_id}'><b>👀{message.from_user.first_name}</b></a> has been muted"
                "\nfor the reason: Profanity."
            )
            return  


async def check_messages_to_spam(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    count_spam: int,
    until_date: datetime
    ) -> None:
    if not message.chat or not message.from_user:
        return

    if message.text is None:  
        return
    
    doc: Doc = nlp_model(message.text)
    user_id: int = message.from_user.id
    lemmas: List[str] = [token.lemma_ for token in doc]
    lemma_counts: Counter[str] = Counter(lemmas)

    old_message: Optional[str] = await get_old_message(
        user_id=user_id,
        message=message.text
    )

    for count in lemma_counts.values():
        messages_count = await get_count_messages(
            user_id=user_id,
            message=message.text
        )

        if count >= count_spam or messages_count >= count_spam or old_message == message.text:
            await message.delete()
            await mute_with_message(
                bot=bot,
                chat_id=message.chat.id,
                user_id=user_id,
                until_date=until_date,
                message_text=f"<a href='tg://user?id={user_id}'><b>👀{message.from_user.first_name}</b></a> has been muted"
                "\nfor the reason: Spamming."
            )
            return 