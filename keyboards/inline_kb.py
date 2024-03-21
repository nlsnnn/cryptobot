from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_RU


def get_markup(width, *args, **kwargs):
    builder = InlineKeyboardBuilder()
    buttons = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button
            ))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button
            ))

    builder.row(*buttons, width=width)
    return builder.as_markup()


def get_url_markup(width, *args, **kwargs):
    builder = InlineKeyboardBuilder()
    buttons = []

    if kwargs:
        for button, url in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button,
                url=url
            ))


    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button
            ))

    builder.row(*buttons, width=width)
    return builder.as_markup()