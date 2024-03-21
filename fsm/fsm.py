from aiogram.fsm.state import State, StatesGroup


class FSMTopUp(StatesGroup):
    fill_txid = State()


class FSMPay(StatesGroup):
    choice_press = State()
    confirm_press = State()