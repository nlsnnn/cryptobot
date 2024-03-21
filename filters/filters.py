from typing import Any
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import orm_check_txid, orm_get_balance
from services.txid_scrap import check_txid
from lexicon.lexicon import LEXICON_RU


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


class ValidBalance(BaseFilter):
    async def __call__(self, callback: CallbackQuery, session: AsyncSession, state: FSMContext):
        balance = await orm_get_balance(session, callback.from_user.id)
        data = await state.get_data()
        amount = data.get('pay_amount')
        if int(amount) <= int(balance):
            return {'amount': amount}
        return False