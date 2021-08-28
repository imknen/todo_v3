from aiogram.dispatcher.filters.state import StatesGroup, State


class RemainderSG(StatesGroup):
    remainder_date = State()
    title = State()
    description = State()
    confirm = State()


class TaskSG(StatesGroup):
    title = State()
    description = State()
    over_date = State()
    confirm = State()
    sub_r_n = State()


class MainSG(StatesGroup):
    create_dialogs = State()
    list_tasks = State()
    view_present= State()


class NoteSG(StatesGroup):
    volume = State()
    confirm = State()
