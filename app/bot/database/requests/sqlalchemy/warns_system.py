from typing import List, Tuple, Optional

from aiogram_i18n import I18nContext
from aiogram.types import User
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import (
    Result, ScalarSelect,
    and_, delete, update
)

from app.bot.database.models import Reasons, Warns
from app.bot.database.session import async_session


async def add_user_warn(
    user_id: int, 
    chat_id: int,
    warns: int = 1
) -> int:
    async with async_session() as session:
        async with session.begin():
            warns_count: Result[Tuple[int]] = await session.execute(
                insert(Warns)
                .values(
                    user_id=user_id,
                    chat_id=chat_id
                )
                .on_conflict_do_update(
                    set_={'warns': Warns.warns + warns},
                    index_elements=[
                        'user_id',
                        'chat_id'
                    ]
                )
                .returning(Warns.warns)
            )

            current_warns: Optional[int] = warns_count.scalar_one_or_none()

            return current_warns


async def add_reason(
    user_id: int, 
    chat_id: int, 
    reason: str
) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                insert(Reasons).values(
                    user_id=user_id, 
                    chat_id=chat_id, 
                    reasons=reason
                )
            )


async def get_user_reasons(
    i18n: I18nContext,
    locale: Optional[str],
    reply_user: User, 
    chat_id: int
) -> Optional[str]:
    async with async_session() as session:
        query: Result[Tuple[Warns]] = await session.execute(
            select(Warns)
            .options(
                selectinload(Warns.reasons)
            )
            .where(
                and_(
                    Warns.user_id == reply_user.id,
                    Warns.chat_id == chat_id
                )
            )
        )

        result: Optional[Warns] = query.scalar_one_or_none()
        if not result:
            return None

        reasons: List[Reasons] = result.reasons
        if not reasons:
            return i18n.get(
                'not-reason',
                locale
            )

        reasons_list: List[str] = [
            i18n.get(
                'warn-reason', 
                locale,
                reason=reason.reason_text
            )
            for reason in reasons
        ]

        joined_reasons: str = "\n".join(reasons_list)
        reasons_message: str = i18n.get(
            'user-reasons',
            locale,
            reasons=joined_reasons,
            warns=result.warns,
            user_id=reply_user.id,
            user_full_name=reply_user.full_name
        )

        return reasons_message


async def delete_user_reason(
    user_id: int, 
    chat_id: int
) -> None:
    async with async_session() as session:
        async with session.begin():
            subquery: ScalarSelect = (
                select(Reasons.id)
                .where(
                    and_(
                        Reasons.user_id == user_id,
                        Reasons.chat_id == chat_id
                    )
                )
                .order_by(Reasons.id.desc()).limit(1)
                .scalar_subquery()
            )

            await session.execute(
                delete(Reasons)
                .where(Reasons.id == subquery)
            )


async def delete_user_reasons(
    user_id: int, 
    chat_id: int
) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                delete(Reasons)
                .where(
                    and_(
                        Reasons.user_id == user_id,
                        Reasons.chat_id == chat_id
                    )
                ) 
            )


async def delete_warn(
    user_id: int, 
    chat_id: int,
    warns: int = 1
) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Warns)
                .values(warns=Warns.warns - warns)
                .where(
                    and_(
                        Warns.user_id == user_id, 
                        Warns.chat_id == chat_id,
                        Warns.warns > 0
                    )
                )
            )