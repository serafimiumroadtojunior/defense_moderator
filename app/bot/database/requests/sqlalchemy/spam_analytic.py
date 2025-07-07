from typing import Tuple, Optional, Union

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.future import select
from sqlalchemy import Result, Row

from app.bot.database.models import SpamAnalitic
from app.bot.database.session import async_session
from app.bot.database.requests.redis import message_counter


async def add_message(
    user_id: int,
    message: str
) -> None:
    count_unique: int = await message_counter(
        user_id=user_id,
        message_text=message
    )

    async with async_session() as session:
        async with session.begin():
            await session.execute(
                insert(SpamAnalitic)
                .values(
                    user_id=user_id,
                    all_count=1,
                    unique_count=1
                )
                .on_conflict_do_update(
                    index_elements=['user_id'],
                    set_={
                        'all_count': SpamAnalitic.all_count + 1,
                        'unique_count': count_unique
                    }
                )
            )


async def count_percentage(user_id: int) -> int:
    async with async_session() as session:
        result: Result[Tuple[int]] = await session.execute(
            select(
                SpamAnalitic.unique_count, 
                SpamAnalitic.all_count
            )
            .where(SpamAnalitic.user_id == user_id)
        )

        row: Union[Row[Tuple[int]], None] = result.first()

        if not row:
            return 0

        unique_count, all_count = row
        return (unique_count / all_count) * 100