from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Integer, UniqueConstraint

from ..session import Base


class Warns(Base):
    __tablename__ = "users_moderations"
    __table_args__ = (
        {"schema" : "warns_system"},
        UniqueConstraint(
            "user_id", 
            "chat_id", 
            name="const_user_chat_unique"
        )
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    warns: Mapped[int] = mapped_column(Integer, default=0, index=True)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)

    reasons = relationship(
        "Reasons", 
        back_populates="user", 
        uselist=True,
        lazy="selectin"
    )