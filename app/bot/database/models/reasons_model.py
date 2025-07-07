from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger, Integer, String, 
    ForeignKeyConstraint, 
    UniqueConstraint
)

from ..session import Base


class Reasons(Base):
    __tablename__ = "warns_reasons"
    __table_args__ = (
        {"schema" : "warns_system"},
        UniqueConstraint(
            "user_id", 
            "chat_id", 
            name="const_user_chat_unique"
        ),
        ForeignKeyConstraint(
            ["user_id"],
            ["users_moderations.user_id"],
            name="const_user_id_fk"
        )
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    reasons: Mapped[str] = mapped_column(String(255))

    user = relationship("Warns", back_populates='reasons')