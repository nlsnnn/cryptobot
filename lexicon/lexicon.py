LEXICON_RU: dict[str: str] = {
    'start': '<b>Чего желаешь?</b>',
    'profile': '<b>Профиль пользователя @{user}</b>\n\nВаш баланс: {balance}$\n'
                'Подписка: {subscription}\n\n<i>Регистрация в боте: {date}</i>',
    'pay': '<b>Выберите подписку</b>',
    'confirm_pay': '<b>{days}</b>\n\n<i>С вашего баланса спишется {amount}$</i>\n\nВаш баланс: {balance}$',
    'pay_done': '<b>Подписка оплачена!</b>',
    'pay_wrong': '<b>Недостаточно денег на балансе!</b>',
    'balance': '<b>Ваш баланс: {balance}$</b>',
    'topup_start': '<b>TRC20 USDT:</b>\n<i>{address}</i>\n\nПосле оплаты отправьте сюда хэш транзакции!',
    'topup_done': '<b>Баланс пополнен на {amount}$!</b>',
    'topup_wrong': '<b>Ошибка хэша!</b> Возможные причины:\n\n'
                    '• Неверный хэш\n• Транзакция еще идет\n• Введен не хэш',
    'other': 'IDK',
    'pay_btn': 'Оплатить 💲',
    'balance_btn': 'Баланс 💰',
    'profile_btn': 'Профиль 🆔',
    'topup_btn': 'Пополнить',
    'd14_btn': ['14 дней - 29$', '14 дней', '29'],
    'd30_btn': ['30 дней - 49$', '30 дней', '49'],
    'confirm_btn': 'Подтверждаю ✔',
    'backward': '❌',
    # PRIVATE
    'private_info': '<b>Все ресурсы для пользователей подписки</b>',
    'private_btn': 'Подписка 🎫',
    'private_channel_btn': 'Канал 👻',
    'private_chat_btn': 'Чат ☁'
}

LINKS: dict[str: str] = {
    'channel': 'https://t.me/+3dxbYNjg_rgxZjUy',
    'chat': 'https://t.me/+Xb5iIIjnfhA4MTQy'
}