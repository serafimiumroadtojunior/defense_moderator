from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger, Integer, String,
    UniqueConstraint, CheckConstraint, 
    ForeignKeyConstraint, PrimaryKeyConstraint
)

from ..session import Base


class Warns(Base):
    __tablename__ = "users_moderations"
    __table_args__ = (
        {"schema" : "warns_system"},
        UniqueConstraint(
            "user_id", "chat_id", 
            name="const_user_chat_unique"
        ),
        PrimaryKeyConstraint(
            "id", 
            name="const_id_primary"
        ),
        CheckConstraint(
            "warns >= 0 and warns <= 3",
            name="const_warns_check"
        )
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)
    warns: Mapped[int] = mapped_column(Integer, default=1, index=True)

    reasons: Mapped[List['Reasons']] = relationship(
        "Reasons", 
        back_populates="user"
    )


class Reasons(Base):
    __tablename__ = "warns_reasons"
    __table_args__ = (
        {"schema" : "warns_system"},
        UniqueConstraint(
            "user_id", "chat_id", 
            name="const_user_chat_unique"
        ),
        ForeignKeyConstraint(
            ["user_id", "chat_id"],
            ["users_moderations.user_id", 
            "users_moderations.chat_id"],
            name="const_user_id_fk"
        )
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)
    reason_text: Mapped[str] = mapped_column(String(255))

    user: Mapped['Warns'] = relationship("Warns", back_populates='reasons')