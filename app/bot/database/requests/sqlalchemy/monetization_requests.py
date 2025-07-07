from typing import Optional, Tuple

from sqlalchemy import Result, Row
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert

from app.bot.database.models import UserChecks
from app.bot.database.session import async_session


async def add_user_check(
    user_id: int,
    stars_amount: int,
    check_id: str
) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                insert(UserChecks)
                .values(
                    user_id=user_id,
                    stars_amount=stars_amount,
                    check_id=check_id
                )
            )


async def get_user_check(user_id: int) -> Optional[Tuple[str, int]]:
    async with async_session() as session:
        async with session.begin():
            result: Result[Tuple[str, int]] = await session.execute(
                select(
                    UserChecks.check_id,
                    UserChecks.stars_amount
                )
                .where(UserChecks.user_id == user_id)
                .order_by(
                    UserChecks.date_donate.desc()
                )
            )

            payment_element: Optional[Row[Tuple[str, int]]] = result.first()

            if not payment_element:
                return None
            
            payment_check: str = payment_element[0]
            payment_amount: int = payment_element[1]

            return payment_check, payment_amount