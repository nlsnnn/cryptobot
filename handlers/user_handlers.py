import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from fsm.fsm import FSMTopUp
from filters.filters import ValidHash
from lexicon.lexicon import LEXICON_RU
from keyboards.inline_kb import get_markup
from database.requests import (orm_add_user, orm_get_balance, orm_update_balance,
                               orm_add_txid)

logger = logging.getLogger(__name__)

user_router = Router()


@user_router.message(CommandStart())
async def start_cmd(message: Message, session: AsyncSession):
    user = message.from_user
    await orm_add_user(
        session=session,
        tg_id=user.id,
        name=user.full_name
    )

    markup = get_markup(2, 'balance_btn', 'pay_btn')
    await message.answer(LEXICON_RU['start'], reply_markup=markup)
    logger.info(f'Пользователь {message.from_user.username} запустил бота')


@user_router.callback_query(F.data == 'balance_btn')
async def balance_check(callback: CallbackQuery, session: AsyncSession):
    balance = await orm_get_balance(session, callback.from_user.id)
    markup = get_markup(1, 'topup_btn', 'backward')
    await callback.message.edit_text(LEXICON_RU['balance'].format(balance=balance),
                                     reply_markup=markup)
    logger.info(f'Пользователь {callback.from_user.username} в меню баланса')


# Пополнение баланса
@user_router.callback_query(F.data == 'topup_btn')
async def topup_start(callback: CallbackQuery, state: FSMContext, address: str):
    markup = get_markup(1, 'backward')
    await callback.message.edit_text(LEXICON_RU['topup_start'].format(address=address),
                                     reply_markup=markup)
    await state.set_state(FSMTopUp.fill_txid)
    logger.info(f'Пользователь {callback.from_user.username} начал пополнять баланс')


# Успешное пополнение баланса
@user_router.message(StateFilter(FSMTopUp.fill_txid), ValidHash())
async def topup_done(message: Message, state: FSMContext, session: AsyncSession, amount: int):
    await orm_update_balance(session, message.from_user.id, amount)
    await orm_add_txid(session, message.text, amount)
    markup = get_markup(1, 'backward')
    await message.answer(LEXICON_RU['topup_done'].format(amount=amount),
                         reply_markup=markup)
    await state.clear()
    logger.info(f'Пользователь {message.from_user.username} успешно пополнил баланс')


# Некорректный хэш
@user_router.message(StateFilter(FSMTopUp.fill_txid))
async def topup_wrong(message: Message):
    markup = get_markup(1, 'backward')
    await message.answer(LEXICON_RU['topup_wrong'],
                         reply_markup=markup)
    logger.info(f'Пользователь {message.from_user.username} ввел некорректный хэш')


# Оплата подписки
@user_router.callback_query(F.data == 'pay_btn')
async def pay_start(callback: CallbackQuery):
    markup = get_markup(2, '14d_btn', '30d_btn', 'backward')
    await callback.message.edit_text(LEXICON_RU['pay'], reply_markup=markup)


@user_router.callback_query(F.data == '14d_btn')
async def pay_14d(callback: CallbackQuery):
    pass


@user_router.callback_query(F.data == 'backward')
async def backward(callback: CallbackQuery):
    markup = get_markup(2, 'balance_btn', 'pay_btn')
    await callback.message.edit_text(LEXICON_RU['start'], reply_markup=markup)