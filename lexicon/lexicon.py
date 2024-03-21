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
    'private_chat_btn': 'Чат ☁',
    # ADMIN
    'admin_start': 'Что интересует?',
    'number_users': 'Количество пользователей: {users}',
    'user_info_fill': 'Введите ID пользователя',
    'user_info': '<b>Профиль пользователя @{user}</b>\n\nВаш баланс: {balance}$\n'
                'Подписка: {subscription}\n\n<i>Регистрация в боте: {date}</i>',
    'user_info_wrong': 'Неверный ID!',
    'set_balance_fill': '<b>Введите новый баланс</b>',
    'set_balance': '<b>Пользователю {user} установлен баланс {balance}$</b>',
    'set_balance_alert': '<b>Администратор установил вам новый баланс!</b>',
    'mailing_fill': '<b>Выберите тип рассылки</b>',
    'mailing_photo': '<b>Отправьте фото</b>',
    'mailing_text': '<b>Введите текст для рассылки</b>',
    'mailing_start': 'Рассылка началась\nБот оповестит когда рассылку закончит',
    'mailing_end': "Рассылка была завершена\n✅ Получили сообщение: {receive_users}\n❌ Заблокировали бота: {block_users}",
    'number_btn': 'Пользователи',
    'mailing_btn': 'Рассылка',
    'user_info_btn': 'Инфо о пользователе',
    'set_balance_btn': 'Установить баланс',
    'photo_btn': 'Картинка 🖼',
    'text_btn': 'Текст 🔠',
    'backward_admin': '❌'
}

LINKS: dict[str: str] = {
    'channel': 'https://t.me/+3dxbYNjg_rgxZjUy',
    'chat': 'https://t.me/+Xb5iIIjnfhA4MTQy'
}