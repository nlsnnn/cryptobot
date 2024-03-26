import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from services.services import text_subscription
from fsm.fsm import FSMTopUp, FSMPay
from filters.filters import ValidHash, ValidBalance
from lexicon.lexicon import LEXICON_RU
from keyboards.inline_kb import get_markup
from database.requests import (orm_add_user, orm_get_balance, orm_add_balance,
                               orm_add_txid, orm_get_days, orm_sub_balance,
                               orm_check_private_user, orm_check_date, orm_set_private_user)

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

    markup = get_markup(2, 'balance_btn', 'pay_btn', 'profile_btn')
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
    await orm_add_balance(session, message.from_user.id, amount)
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
async def pay_start(callback: CallbackQuery, state: FSMContext):
    markup = get_markup(2, d14_btn=LEXICON_RU['d14_btn'][0], d30_btn=LEXICON_RU['d30_btn'][0])
    await callback.message.edit_text(LEXICON_RU['pay'], reply_markup=markup)
    await state.set_state(FSMPay.choice_press)
    logger.info(f'Пользователь {callback.from_user.username} выбирает подписку')


# Подтверждение оплаты
@user_router.callback_query(StateFilter(FSMPay.choice_press))
async def pay_confirm(callback: CallbackQuery, session: AsyncSession, state: FSMContext):
    n_data = callback.data
    await state.update_data(pay_amount=LEXICON_RU[n_data][2],
                            days=LEXICON_RU[n_data][3])
    balance = await orm_get_balance(session, callback.from_user.id)
    markup = get_markup(2, 'confirm_btn', 'backward')
    await callback.message.edit_text(LEXICON_RU['confirm_pay'].format(
        days=LEXICON_RU[n_data][1],
        amount=LEXICON_RU[n_data][2],
        balance=balance
    ), reply_markup=markup)
    await state.set_state(FSMPay.confirm_press)
    logger.info(f'Пользователь {callback.from_user.username} подтверждает оплату')


# Успешная оплата
@user_router.callback_query(StateFilter(FSMPay.confirm_press), F.data == 'confirm_btn', ValidBalance())
async def pay_done(callback: CallbackQuery, session: AsyncSession,
                   state: FSMContext, amount: int, days: int):
    await orm_sub_balance(session, callback.from_user.id, amount)
    await orm_set_private_user(session, callback.from_user.id, days=days)
    markup = get_markup(1, 'backward')
    await callback.message.edit_text(LEXICON_RU['pay_done'], reply_markup=markup)
    await state.clear()

    logger.info(f'Пользователь {callback.from_user.username} успешно оплатил подписку')


# Недостаточно денег
@user_router.callback_query(StateFilter(FSMPay.confirm_press), F.data == 'confirm_btn')
async def pay_wrong(callback: CallbackQuery):
    markup = get_markup(1, 'backward')
    await callback.message.edit_text(LEXICON_RU['pay_wrong'], reply_markup=markup)
    logger.info(f'Пользователь {callback.from_user.username} не имеет достаточно денег для оплаты')


@user_router.callback_query(F.data == 'profile_btn')
async def profile_press(callback: CallbackQuery, session: AsyncSession):
    balance = await orm_get_balance(session, callback.from_user.id)
    flag = text_subscription(await orm_check_private_user(session, callback.from_user.id))
    date = await orm_check_date(session, callback.from_user.id)
    days = await orm_get_days(session, callback.from_user.id)
    markup = get_markup(1, 'backward')
    await callback.message.edit_text(LEXICON_RU['profile'].format(
        user=callback.from_user.username,
        balance=balance,
        subscription=flag,
        days=days,
        date=date
    ), reply_markup=markup)
    logger.info(f'Пользователь {callback.from_user.username} в меню профиля')


@user_router.callback_query(F.data == 'backward')
async def backward(callback: CallbackQuery):
    markup = get_markup(2, 'balance_btn', 'pay_btn', 'profile_btn')
    await callback.message.edit_text(LEXICON_RU['start'], reply_markup=markup)
    logger.info(f'Пользователь {callback.from_user.username} в главном меню')