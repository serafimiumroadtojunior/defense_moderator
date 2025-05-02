from typing import Optional, Tuple

from sqlalchemy import Result
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert

from app.bot.database.models import Welcome
from app.bot.database.session import async_session


async def add_rules_id(
    chat_id: int, 
    message_id: int
) -> None:
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                insert(Welcome)
                .values(
                    chat_id=chat_id,
                    message_id=message_id
                )
                .on_conflict_do_update(
                    index_elements=['chat_id'],
                    set_={
                        'message_id': message_id
                    }
                )
            )


async def get_message_id(chat_id: int) -> Optional[int]:
    async with async_session() as session:
        async with session.begin():
            result: Result[Tuple[int]] = await session.execute(
                select(Welcome.message_id)
                .where(Welcome.chat_id == chat_id)
            )

            existing_id: Optional[int] = result.scalar()

            if existing_id:
                return existing_id  
            return None