from sqlalchemy import BigInteger, SmallInteger, DateTime, String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(150), nullable=True)
    balance: Mapped[int] = mapped_column(SmallInteger)
    private: Mapped[bool] = mapped_column(Boolean)


class Hash(Base):
    __tablename__ = 'hash'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    txid: Mapped[str] = mapped_column(String(200))
    amount: Mapped[int] = mapped_column(SmallInteger)