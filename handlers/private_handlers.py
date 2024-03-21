import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from lexicon.lexicon import LEXICON_RU
from filters.filters import IsPrivate
from keyboards.inline_kb import get_markup


private_router = Router()
private_router.message.filter(IsPrivate())

logger = logging.getLogger(__name__)