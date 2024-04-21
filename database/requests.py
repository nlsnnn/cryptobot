from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from database.models import Base, User, Hash
from config.config_data import Config, load_config


config: Config = load_config('.env')

engine = create_async_engine(config.db.url, echo=True)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def orm_add_user(
        session: AsyncSession,
        tg_id: int,
        name: str | None = None,
        balance: int = 0,
        private: bool = False
):
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(tg_id=tg_id, name=name, balance=balance, private=private)
        )
        await session.commit()


async def orm_get_balance(
        session: AsyncSession,
        tg_id: int
):
    query = select(User.balance).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_add_balance(
        session: AsyncSession,
        tg_id: int,
        amount: int
):
    query = (update(User).where(User.tg_id == tg_id).values(balance=User.balance + amount))
    await session.execute(query)
    await session.commit()


async def orm_sub_balance(
        session: AsyncSession,
        tg_id: int,
        amount: int
):
    query = (update(User).where(User.tg_id == tg_id).values(balance=User.balance - amount))
    await session.execute(query)
    await session.commit()


async def orm_check_date(
        session: AsyncSession,
        tg_id: int
):
    query = select(User.created).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()


# Hash

async def orm_add_txid(
        session: AsyncSession,
        txid: str,
        amount: int
):
    session.add(Hash(
        txid=txid,
        amount=amount))
    await session.commit()


async def orm_check_txid(
        session: AsyncSession,
        txid: str
):
    query = select(Hash).where(Hash.txid == txid)
    result = await session.execute(query)
    if result.first() is None:
        return True
    return False


# PRIVATE

async def orm_set_private_user(
        session: AsyncSession,
        tg_id: int,
        days: int
):
    query = (update(User).where(User.tg_id == tg_id).values(private=True, days=days))
    await session.execute(query)
    await session.commit()


async def orm_delete_private_user(
        session: AsyncSession,
        tg_id: int
):
    query = (update(User).where(User.tg_id == tg_id).values(private=False))
    await session.execute(query)
    await session.commit()


async def orm_check_private_user(
        session: AsyncSession,
        tg_id: int
):
    query = select(User.private).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_id_private_users(
        session: AsyncSession
):
    query = select(User.tg_id).where(User.private == True)
    result = await session.execute(query)
    return result.all()


async def orm_get_id_expired_private_users(
        session: AsyncSession
):
    query = select(User.tg_id).where(User.private == True, User.days <= 1)
    result = await session.execute(query)
    return result.all()


async def orm_sub_day(
        session: AsyncSession,
        tg_id: int
):
    query = (update(User).where(User.tg_id == tg_id).values(days=User.days - 1))
    await session.execute(query)
    await session.commit()


async def orm_get_days(
        session: AsyncSession,
        tg_id: int
):
    query = select(User.days).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()


# ADMIN

async def orm_get_number_users(
        session: AsyncSession
):
    query = func.count(User.id)
    result = await session.execute(query)
    return result.scalar()


async def orm_get_id_users(
        session: AsyncSession
):
    query = select(User.tg_id)
    result = await session.execute(query)
    return result.all()


async def orm_get_users(
        session: AsyncSession
):
    query = select(User.tg_id, User.name)
    result = await session.execute(query)
    return result.all()


async def orm_set_balance(
        session: AsyncSession,
        tg_id: int,
        amount: int
):
    query = (update(User).where(User.tg_id == tg_id).values(balance=amount))
    await session.execute(query)
    await session.commit()