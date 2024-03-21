import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU, LINKS
from filters.filters import IsPrivate
from keyboards.inline_kb import get_markup, get_url_markup


private_router = Router()
private_router.message.filter(IsPrivate())
private_router.callback_query.filter(IsPrivate())

logger = logging.getLogger(__name__)


@private_router.message(CommandStart())
async def private_start_cmd(message: Message, session: AsyncSession):
    markup = get_markup(3, 'balance_btn', 'pay_btn', 'profile_btn', 'private_btn')
    await message.answer(LEXICON_RU['start'], reply_markup=markup)
    logger.info(f'Пользователь {message.from_user.username} запустил бота (PRIVATE)')


@private_router.callback_query(F.data == 'private_btn')
async def private_info(callback: CallbackQuery):
    markup = get_url_markup(2,
                            'backward',
                            private_channel_btn=LINKS['channel'],
                            private_chat_btn=LINKS['chat'])
    await callback.message.edit_text(LEXICON_RU['private_info'], reply_markup=markup)
    logger.info(f'Пользователь {callback.from_user.username} в меню подписки (PRIVATE)')


@private_router.callback_query(F.data == 'backward')
async def private_backward(callback: CallbackQuery):
    markup = get_markup(3, 'balance_btn', 'pay_btn', 'profile_btn', 'private_btn')
    await callback.message.edit_text(LEXICON_RU['start'], reply_markup=markup)
    logger.info(f'Пользователь {callback.from_user.username} в главном меню (PRIVATE)')