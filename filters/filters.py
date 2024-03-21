from typing import Any
from aiogram.types import Message
from aiogram.filters import BaseFilter
from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import orm_check_txid
from services.txid_scrap import check_txid


class ValidHash(BaseFilter):
    async def __call__(self, message: Message, session: AsyncSession):
        if len(message.text) != 64:
            return False
        if not (await orm_check_txid(session, message.text)):
            return False
        amount = check_txid(txid=message.text)
        if amount:
            return {'amount': amount}
        return False