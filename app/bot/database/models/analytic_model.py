from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, Integer

from ..session import Base


class SpamAnalitic(Base):
    __tablename__ = "spam_analytic"
    __table_args__ = (
        {"schema" : "analytic"}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    all_count: Mapped[int] = mapped_column(Integer, default=0)
    unique_count: Mapped[int] = mapped_column(Integer, default=0)