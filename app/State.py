from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    name = State()
    age = State()
    number = State()

class Buy_ak(StatesGroup):
    count = State()
    ak = State()
    id = State()