from aiogram.fsm.state import State, StatesGroup


class FSMTopUp(StatesGroup):
    fill_txid = State()