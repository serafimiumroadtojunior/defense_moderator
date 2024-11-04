from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..session import Base


class Warns(Base):
    __tablename__ = "users_moderations"
    __table_args__ = {"schema" : "warns_system"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    warns: Mapped[int] = mapped_column(Integer, default=0)