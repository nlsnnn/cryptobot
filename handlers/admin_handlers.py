import logging
import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, PhotoSize
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from sqlalchemy.ext.asyncio import AsyncSession

from fsm.fsm import FSMUserInfo, FSMMailing
from lexicon.lexicon import LEXICON_RU
from filters.filters import IsAdmin, ValidID
from keyboards.inline_kb import get_markup

from database.requests import (orm_check_date, orm_check_private_user,
                               orm_get_balance, orm_get_number_users,
                               orm_set_balance, orm_get_id_users)
from services.services import text_subscription


admin_router = Router()
admin_router.message.filter(IsAdmin())

logger = logging.getLogger(__name__)


@admin_router.message(Command('admin'))
async def auth_admin(message: Message):
    markup = get_markup(2, 'number_btn', 'user_info_btn', 'mailing_btn')
    await message.delete()
    await message.answer(LEXICON_RU['admin_start'], reply_markup=markup)


@admin_router.callback_query(F.data == 'number_btn')
async def number_users(callback: CallbackQuery, session: AsyncSession):
    users = await orm_get_number_users(session)
    markup = get_markup(1, 'backward_admin')
    await callback.message.edit_text(LEXICON_RU['number_users'].format(users=users),
                                     reply_markup=markup)


@admin_router.callback_query(F.data == 'user_info_btn')
async def user_info_start(callback: CallbackQuery, state: FSMContext):
    markup = get_markup(1, 'backward_admin')
    await callback.message.edit_text(LEXICON_RU['user_info_fill'], reply_markup=markup)
    await state.set_state(FSMUserInfo.fill_id)


@admin_router.message(StateFilter(FSMUserInfo.fill_id), ValidID())
async def user_info(message: Message, state: FSMContext, session: AsyncSession):
    user_id = message.text
    await state.update_data(tg_id=user_id)
    balance = await orm_get_balance(session, user_id)
    flag = text_subscription(await orm_check_private_user(session, user_id))
    date = await orm_check_date(session, user_id)
    markup = get_markup(1, 'set_balance_btn', 'backward_admin')
    await message.delete()
    await message.answer(LEXICON_RU['profile'].format(
        user=user_id,
        balance=balance,
        subscription=flag,
        date=date
    ), reply_markup=markup)
    await state.set_state(default_state)


@admin_router.callback_query(F.data == 'set_balance_btn')
async def set_balance_start(callback: CallbackQuery, state: FSMContext):
    markup = get_markup(1, 'backward_admin')
    await callback.message.answer(LEXICON_RU['set_balance_fill'], reply_markup=markup)
    await state.set_state(FSMUserInfo.fill_amount)


@admin_router.message(StateFilter(FSMUserInfo.fill_amount), ValidID())
async def set_balance(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    tg_id = data.get('tg_id')
    await orm_set_balance(session, tg_id, message.text)
    markup = get_markup(1, 'backward_admin')
    await message.delete()
    await message.answer(LEXICON_RU['set_balance'].format(
        user=tg_id, balance=message.text
    ), reply_markup=markup)
    await state.clear()


@admin_router.message(StateFilter(FSMUserInfo.fill_id))
async def user_info_wrong(message: Message):
    markup = get_markup(1, 'backward_admin')
    await message.delete()
    await message.answer(LEXICON_RU['user_info_wrong'], reply_markup=markup)


@admin_router.callback_query(F.data == 'mailing_btn')
async def mailing(callback: CallbackQuery):
    markup = get_markup(2, 'photo_btn', 'text_btn', 'backward_admin')
    await callback.message.edit_text(LEXICON_RU['mailing_fill'], reply_markup=markup)


@admin_router.callback_query(F.data == 'text_btn')
async def mailing_text(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['mailing_text'])
    await state.set_state(FSMMailing.fill_text)


@admin_router.callback_query(F.data == 'photo_btn')
async def mailing_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['mailing_photo'])
    await state.set_state(FSMMailing.upload_photo)


@admin_router.message(StateFilter(FSMMailing.upload_photo),
                      F.photo[-1].as_('largest_photo'))
async def mailing_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize):
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id
    )
    await message.delete()
    await message.answer(LEXICON_RU['mailing_text'])
    await state.set_state(FSMMailing.fill_text)


@admin_router.message(StateFilter(FSMMailing.fill_text))
async def mailing_start(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    if data:
        photo = data.get('photo_id')
    markup = get_markup(1, 'backward_admin')
    await message.delete()
    await message.answer(LEXICON_RU['mailing_start'])
    ids = await orm_get_id_users(session)
    users = [int(item) for tuple_item in ids for item in tuple_item]
    receive_users, block_users = 0, 0
    for user in users:
        try:
            # await message.bot.send_message()
            await message.bot.send_photo(user, photo=photo, caption=message.text)
            receive_users += 1
        except:
            block_users += 1
        await asyncio.sleep(0.4)
    await message.answer(LEXICON_RU['mailing_end'].format(receive_users=receive_users,
                                                          block_users=block_users),
                         reply_markup=markup)
    await state.clear()


@admin_router.callback_query(F.data == 'backward_admin')
async def backward(callback: CallbackQuery):
    markup = get_markup(2, 'number_btn', 'user_info_btn', 'mailing_btn')
    await callback.message.edit_text(LEXICON_RU['admin_start'], reply_markup=markup)