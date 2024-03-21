import logging
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from lexicon.lexicon import LEXICON_RU
from keyboards.inline_kb import get_markup
from sqlalchemy.ext.asyncio import AsyncSession
from database.requests import orm_add_user, orm_get_balance

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


@user_router.callback_query(F.data == 'backward')
async def backward(callback: CallbackQuery):
    markup = get_markup(2, 'balance_btn', 'pay_btn')
    await callback.message.edit_text(LEXICON_RU['start'], reply_markup=markup)