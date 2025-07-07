from collections import Counter
from datetime import datetime
from typing import List, Optional

from redis.asyncio.client import Redis
from spacy.language import Language
from spacy.tokens import Doc
from aiogram import Bot
from aiogram_i18n import I18nContext
from aiogram.types import (
    Chat, Message, 
    User, MessageReactionUpdated,
    ReactionTypeEmoji, ChatMemberUpdated
)

from app.bot.keyboards import ModerationCallback
from ..helpers import (
    mute_with_message, 
    ban_with_message
)
from app.bot.database import (
    get_count_messages, get_old_message,
    get_count_reactions, count_percentage,
    add_message
)


async def unique_messages_spam(
    bot: Bot,
    redis: Redis,
    locale: Optional[str],
    i18n: I18nContext,
    message: Message,
    nlp_model: Language,
    until_date: datetime
) -> None:
    if not message.from_user:
        return None
    
    if not message.text:
        return None
    
    chat: Chat = message.chat
    user: User = message.from_user
    doc: Doc = nlp_model(message.text)
    lemmas_message: str = " ".join([token.lemma_ for token in doc])
    old_message: Optional[str] = await get_old_message(
        redis=redis,
        user_id=user.id,
        chat_id=chat.id,
        message=lemmas_message
    )

    if old_message == lemmas_message:
        await mute_with_message(
            bot=bot,
            redis=redis,
            locale=locale,
            i18n=i18n,
            until_date=until_date,
            chat_id=chat.id,
            user_id=user.id,
            buttons_level=1,
            button_texts=['Unmute✔️'],
            callback_datas=[
                ModerationCallback(
                    action='unmute',
                    user_id=user.id
                ).pack()
            ],
            message_text=i18n.get(
                'unique-messages',
                locale,
                user_id=user.id,
                user_full_name=user.full_name
            )
        )


async def count_messages_spam(
    bot: Bot,
    redis: Redis,
    locale: Optional[str],
    i18n: I18nContext,
    message: Message,
    nlp_model: Language,
    count_spam: int,
    until_date: datetime
) -> None:
    if not message.from_user:
        return None 
    
    if not message.text:
        return None
    
    chat: Chat = message.chat
    user: User = message.from_user
    doc: Doc = nlp_model(message.text)
    lemmas_message: str = " ".join([token.lemma_ for token in doc])
    count_messages: int = await get_count_messages(
        redis=redis,
        user_id=user.id,
        chat_id=chat.id,
        message=lemmas_message
    )

    await add_message(
        user_id=user.id,
        message=lemmas_message
    )

    if count_messages >= count_spam:
        await mute_with_message(
            bot=bot,
            redis=redis,
            locale=locale,
            i18n=i18n,
            chat_id=chat.id,
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
                "spam-percent-ban",
                locale,
                user_id=user.id,
                user_full_name=user.full_name,
                count_spam=count_spam
            )
        )


async def unique_words_spam(
    bot: Bot,
    redis: Redis,
    locale: Optional[str],
    i18n: I18nContext,
    message: Message,
    nlp_model: Language,
    until_date: datetime,
    count_spam: int    
) -> None:
    if not message.from_user:
        return None

    if not message.text:
        return None

    user: User = message.from_user
    chat: Chat = message.chat
    doc: Doc = nlp_model(message.text)
    words_message: List[str] = [token.text for token in doc]
    word_counts: Counter = Counter(words_message)

    for count in word_counts.values():
        if count >= count_spam:
            await mute_with_message(
                bot=bot,
                redis=redis,
                locale=locale,
                i18n=i18n,
                chat_id=chat.id,
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
                    'unique-words',
                    locale,
                    user_id=user.id,
                    user_full_name=user.full_name
                )
            )


async def count_reactions_spam(
    bot: Bot,
    redis: Redis,
    locale: Optional[str],
    i18n: I18nContext,
    reactions: MessageReactionUpdated,
    until_date: datetime,
    count_spam: int   
) -> None:
    for reaction in reactions.new_reaction:
        if not isinstance(reaction, ReactionTypeEmoji):
            return None

        if not reactions.user:
            return None

        user: User = reactions.user
        chat: Chat = reactions.chat
        emoji: str = reaction.emoji
        count: int = await get_count_reactions(
            redis=redis,
            user_id=user.id,
            chat_id=chat.id,
            emoji=emoji
        )

        if count >= count_spam:
            await ban_with_message(
                bot=bot,
                locale=locale,
                i18n=i18n,
                chat_id=chat.id,
                user_id=user.id,
                until_date=until_date,
                buttons_level=1,
                button_texts=['Unban✔️'],
                callback_datas=[
                    ModerationCallback(
                        action='unban',
                        user_id=user.id
                    ).pack()
                ],
                message_text=i18n.get(
                    "banned-reactions",
                    locale,
                    user_id=user.id,
                    user_full_name=user.full_name
                )
            )


async def parse_messages_percent(
    bot: Bot,
    locale: Optional[str],
    i18n: I18nContext,
    member: ChatMemberUpdated,
    spam_percent: float = 60.0
) -> None:
    chat: Chat = member.chat
    new_member = member.new_chat_member
    old_member = member.old_chat_member
    user: User = member.from_user

    if new_member.status == "member" or old_member.status == "member":
        messages_percent: int = await count_percentage(
            user_id=user.id
        )

        if messages_percent > spam_percent:
            await ban_with_message(
                bot=bot,
                locale=locale,
                i18n=i18n,
                chat_id=chat.id,
                user_id=user.id,
                until_date=None,
                buttons_level=1,
                button_texts=['Unban✔️'],
                callback_datas=[
                    ModerationCallback(
                        action='unban',
                        user_id=user.id
                    ).pack()
                ],
                message_text=i18n.get(
                    "spam-percent-ban",
                    locale,
                    user_id=user.id,
                    user_full_name=user.full_name
                )
            )