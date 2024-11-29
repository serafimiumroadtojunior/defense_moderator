from sqlalchemy import BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from ..session import Base


class Welcome(Base):
    __tablename__ = "welcome_users"
    __table_args__ = {"schema" : "users"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)