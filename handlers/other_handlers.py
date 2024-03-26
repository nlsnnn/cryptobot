from aiogram import Router
from aiogram.types import Message
from keyboards.inline_kb import get_markup
from lexicon.lexicon import LEXICON_RU

other_router = Router()


@other_router.message()
async def other_msg(message: Message):
    await message.delete()
    markup = get_markup(1, 'backward')
    await message.answer(LEXICON_RU['other'], reply_markup=markup)