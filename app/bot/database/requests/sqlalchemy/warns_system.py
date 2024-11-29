from typing import List, Optional, Tuple, Union

from sqlalchemy import Insert, Result, ScalarSelect, and_, delete, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select

from app.bot.database.models import Reasons, Warns
from app.bot.database.session import async_session


async def add_user(user_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            new_user: Insert = insert(Warns).values(user_id=user_id).on_conflict_do_nothing(
                index_elements=['user_id']
            )
            await session.execute(new_user)


async def add_reason(user_id: int, reason: str) -> None:
    async with async_session() as session:
        async with session.begin():
            new_reason: Insert = insert(Reasons).values(user_id=user_id, reasons=reason)
            await session.execute(new_reason)


async def get_user_reasons(user_id: int) -> Union[List[str], str]:
    async with async_session() as session:
        result: Result[Tuple[str]] = await session.execute(
            select(Reasons.reasons)
            .where(Reasons.user_id == user_id)
        )

        reasons: List[str] = [f"📝<b>Reason for warn: {reason}</b>" for reason in result.scalars()]
        
        if not reasons:
            return "<b>No reasons for warns found.</b>"
        return "\n".join(reasons)  


async def delete_user_reason(user_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            subquery: ScalarSelect = select(Reasons.id).where(Reasons.user_id == user_id).order_by(Reasons.id.desc()).limit(1).scalar_subquery()
            await session.execute(
                delete(Reasons)
                .where(Reasons.id == subquery)
            )


async def delete_user_reasons(user_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                delete(Reasons)
                .where(Reasons.user_id == user_id) 
            )


async def add_warn(user_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Warns)
                .where(and_(Warns.user_id == user_id, Warns.warns < 3))
                .values(warns=Warns.warns + 1)
            )


async def reset_warns(user_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Warns)
                .where(Warns.user_id == user_id)
                .values(warns=0)
            )


async def check_warns(user_id: int) -> int:
    async with async_session() as session:
        result: Result[Tuple[int]] = await session.execute(
            select(Warns.warns)
            .where(Warns.user_id == user_id)
        )

        warns: Optional[int] = result.scalar_one_or_none()
        return warns if warns else 0


async def delete_warn(user_id: int) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Warns)
                .where(and_(Warns.user_id == user_id, Warns.warns > 0))
                .values(warns=Warns.warns - 1)
            )