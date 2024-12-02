from typing import List, Tuple

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy import (
    Insert, Result, ScalarSelect,
    and_, delete, update
)

from app.bot.database.models import Reasons, Warns
from app.bot.database.session import async_session


async def add_user(user_id: int, chat_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                insert(Warns)
                .values(
                    user_id=user_id,
                    chat_id=chat_id
                )
                .on_conflict_do_nothing(
                    index_elements=[
                        'user_id',
                        'chat_id'
                    ]
                )
            )


async def add_reason(user_id: int, chat_id: int, reason: str) -> None:
    async with async_session() as session:
        async with session.begin():
            new_reason: Insert = insert(Reasons).values(
                user_id=user_id, 
                chat_id=chat_id, 
                reasons=reason
            )

            await session.execute(new_reason)


async def get_user_reasons(user_id: int, chat_id: int) -> str:
    async with async_session() as session:
        result: Result[Tuple[str]] = await session.execute(
            select(Reasons.reasons)
            .where(
                and_(
                    Reasons.user_id == user_id,
                    Reasons.chat_id == chat_id
                )
            )
        )

        reasons: List[str] = [f"📝<b>Reason for warn: {reason}</b>" for reason in result.scalars()]
        
        if not reasons:
            return "<b>No reasons for warns found.</b>"
        return "\n".join(reasons)  


async def delete_user_reason(user_id: int, chat_id: int) -> None:
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


async def delete_user_reasons(user_id: int, chat_id: int) -> None:
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


async def add_warn(user_id: int, chat_id: int) -> int:
    async with async_session() as session:
        async with session.begin():
            warns: Result[Tuple[int]] = await session.execute(
                update(Warns)
                .values(warns=Warns.warns + 1)
                .returning(Warns.warns)
                .where(
                    and_(
                    Warns.user_id == user_id, 
                    Warns.chat_id == chat_id,
                    Warns.warns < 3
                    )
                )
            )

            current_warns: int = warns.scalar_one()
            return current_warns


async def reset_warns(user_id: int, chat_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Warns)
                .values(warns=0)
                .where(
                    and_(
                        Warns.user_id == user_id,
                        Warns.chat_id == chat_id
                    )
                )
            )


async def delete_warn(user_id: int, chat_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Warns)
                .values(warns=Warns.warns - 1)
                .where(
                    and_(
                        Warns.user_id == user_id, 
                        Warns.chat_id == chat_id,
                        Warns.warns > 0
                    )
                )
            )