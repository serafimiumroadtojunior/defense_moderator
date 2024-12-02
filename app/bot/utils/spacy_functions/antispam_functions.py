from collections import Counter
from datetime import datetime
from typing import List, Optional

from spacy.language import Language
from spacy.tokens import Doc
from aiogram import Bot
from aiogram.types import (
    Chat, Message, 
    User, MessageReactionUpdated,
    ReactionTypeEmoji
)

from ..helpers import (
    mute_with_message, 
    ban_with_message
)
from app.bot.database import (
    get_count_messages, get_old_message,
    get_count_reactions
)


async def unique_messages_spam(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    until_date: datetime
) -> None:
    if not message.chat or not message.from_user:
        return
    
    if not message.text:
        return
    
    chat: Chat = message.chat
    user: User = message.from_user
    doc: Doc = nlp_model(message.text)
    lemmas_message: str = " ".join([token.lemma_ for token in doc])

    old_message: Optional[str] = await get_old_message(
        user_id=user.id,
        chat_id=chat.id,
        message=lemmas_message
    )

    if old_message == lemmas_message:
        await mute_with_message(
            bot=bot,
            chat_id=chat.id,
            user_id=user.id,
            until_date=until_date,
            message_text=(
                f'<a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
                'has been muted due to repeated messages'
            )
        )


async def count_messages_spam(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    count_spam: int,
    until_date: datetime
) -> None:
    if not message.chat or not message.from_user:
        return
    
    if not message.text:
        return
    
    chat: Chat = message.chat
    user: User = message.from_user
    doc: Doc = nlp_model(message.text)
    lemmas_message: str = " ".join([token.lemma_ for token in doc])

    count_messages: int = await get_count_messages(
        user_id=user.id,
        chat_id=chat.id,
        message=lemmas_message
    )

    if count_messages >= count_spam:
        await mute_with_message(
            bot=bot,
            chat_id=chat.id,
            user_id=user.id,
            until_date=until_date,
            message_text=(
                f'<a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
                'has been muted due to spamming'
            )
        )


async def unique_words_spam(
    bot: Bot,
    message: Message,
    nlp_model: Language,
    until_date: datetime,
    count_spam: int    
) -> None:
    if not message.chat or not message.from_user:
        return

    if not message.text:
        return

    user: User = message.from_user
    doc: Doc = nlp_model(message.text)
    words_message: List[str] = [token.text for token in doc]
    word_counts: Counter = Counter(words_message)

    for count in word_counts.values():
        if count >= count_spam:
            await mute_with_message(
                bot=bot,
                chat_id=message.chat.id,
                user_id=user.id,
                until_date=until_date,
                message_text=(
                    f'<a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
                    'has been muted due to repeated words'
                )
            )
            return


async def count_reactions_spam(
    bot: Bot,
    reactions: MessageReactionUpdated,
    until_date: datetime,
    count_spam: int   
) -> None:
    for reaction in reactions.new_reaction:
        if not isinstance(reaction, ReactionTypeEmoji):
            return

        if not reactions.chat or not reactions.user:
            return

        user: User = reactions.user
        chat: Chat = reactions.chat
        emoji: str = reaction.emoji 

        count: int = await get_count_reactions(
            user_id=user.id,
            chat_id=chat.id,
            emoji=emoji
        )

        if count >= count_spam:
            await ban_with_message(
                bot=bot,
                chat_id=chat.id,
                user_id=user.id,
                until_date=until_date,
                message_text=(
                    f'<a href="tg://user?id={user.id}"><b>👀{user.full_name}</b></a>'
                    'has been banned due to spamming reactions'
                )
            )
            return