from aiogram.fsm.state import State, StatesGroup


class FSMTopUp(StatesGroup):
    fill_txid = State()


class FSMPay(StatesGroup):
    choice_press = State()
    confirm_press = State()


class FSMUserInfo(StatesGroup):
    fill_id = State()
    fill_amount = State()


class FSMMailing(StatesGroup):
    fill_text = State()
    upload_photo = State()