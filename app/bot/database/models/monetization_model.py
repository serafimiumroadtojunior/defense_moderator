from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    BigInteger, Integer, 
    UniqueConstraint, String,
    Date
)

from ..session import Base


class UserChecks(Base):
    __tablename__ = "users_checks"
    __table_args__ = (
        {"schema": "monetization_system"},
        UniqueConstraint(
            "user_id",
            name="const_user_unique"
        )
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    stars_amount: Mapped[int] = mapped_column(Integer)
    check_id: Mapped[str] = mapped_column(String)
    date_donate: Mapped[datetime] = mapped_column(Date, default=datetime.now)