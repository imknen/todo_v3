from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Back, Next, SwitchTo
from aiogram_dialog import Dialog, DialogManager, Window, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.kbd import Calendar
from typing import Any
from datetime import date, datetime
from .states_dialog import RemainderSG
from base.my_requests import add_remainder


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        "data_remainder": dialog_manager.current_context().dialog_data.get("data_remainder")
    }


async def add_data(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["data_remainder"].append(m.text)
    await dialog.next(manager)


async def on_date_selected(c: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    manager.current_context().dialog_data["data_remainder"].append(selected_date)
    await c.answer(f'Дата выбрана {selected_date.strftime("%d %B %Y")}')
    await manager.dialog().next(manager)


async def on_start_remainder(start_data: Data, manager: DialogManager):
    manager.current_context().dialog_data["data_remainder"] = []


async def on_finish(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().dialog_data["id_remainder"] = add_remainder((await get_data(manager)).get('data_remainder'))
    await manager.done({'id_remainder': manager.current_context().dialog_data["id_remainder"]})


create_remainder = Dialog(
    Window(
        Calendar(id='calendar', on_click=on_date_selected),
        Const('Укажите дату напоминания.'),
        state=RemainderSG.remainder_date,
        preview_add_transitions=[Next()]
    ),
    Window(
        Const('Введите заголовок напоминания'),
        MessageInput(add_data),
        state=RemainderSG.title,
        preview_add_transitions=[Next()]
    ),
    Window(
        Const('Введите текст сообщения для напоминания.'),
        MessageInput(add_data),
        state=RemainderSG.description,
        preview_add_transitions=[Next()]
    ),
    Window(
        Format('Вы ввели:\n{data_remainder}\nВсё так?'),
        Button(Const("Сохранить"), id='qwerty', on_click=on_finish),
        SwitchTo(Const("Хочу изменить"),
                 id='upd',
                 state=RemainderSG.title),
        preview_add_transitions=[Cancel()],
        state=RemainderSG.confirm,
        getter=get_data,
    ),
    on_start=on_start_remainder
)
