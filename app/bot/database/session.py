import os
from typing import Optional

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase

load_dotenv(dotenv_path=os.path.join("defense_moderator", ".env"))


DATABASE_URL: Optional[str] = os.getenv(key="DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError("No DATABASE_URL provided in environment variables.")

engine: AsyncEngine = create_async_engine(url=DATABASE_URL)
async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass