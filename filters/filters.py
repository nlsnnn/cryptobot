from typing import Any
from aiogram.types import Message
from aiogram.filters import BaseFilter
from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import orm_check_txid
from services.txid_scrap import check_txid


class IsHash(BaseFilter):
    async def __call__(self, message: Message):
        return len(message.text) == 64


class HashFilter(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession):
        return (await orm_check_txid(session, message.text))


class ValidHash(BaseFilter):
    async def __call__(self, message: Message):
        amount = check_txid(txid=message.text)
        if amount:
            return {'amount': amount}
        return False