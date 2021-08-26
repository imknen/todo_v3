from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Back, Start, Next, Group, SwitchTo
from aiogram_dialog import Dialog, DialogManager, Window, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message, CallbackQuery
from aiogram_dialog.widgets.kbd import Calendar
from typing import Any
from datetime import date, datetime

from .states_dialog import TaskSG, RemainderSG, NoteSG
from base.my_requests import get_task, add_task
from base.my_requests import note_link_to_task, remainder_link_to_task


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        "id_note": dialog_manager.current_context().dialog_data.get("id_note"),
        "id_remainder": dialog_manager.current_context().dialog_data.get("id_remainder"),
        "data_task": dialog_manager.current_context().dialog_data.get("data_task"),
    }


async def cancel_info(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.answer('Как хотите.')
    await manager.dialog().next(manager)


async def on_run_dialog(start_data: Data, manager: DialogManager):
    manager.current_context().dialog_data["data_task"] = []
    manager.current_context().dialog_data["id_remainder"] = None
    manager.current_context().dialog_data["id_note"] = None


async def add_to_task(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["data_task"].append(m.text)
    await dialog.next(manager)


async def save_task(c: CallbackQuery, button: Button, manager: DialogManager):
    id_t = add_task(manager.current_context().dialog_data['data_task'])
    manager.current_context().dialog_data["id_task"] = id_t
    await c.answer('Задача сохранена')
    await manager.dialog().next(manager)


async def on_date_selected(c: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    manager.current_context().dialog_data["data_task"].append(selected_date)
    await c.answer(f'{selected_date.strftime("%d %B %Y")}')
    await manager.dialog().next(manager)


async def process_result(start_data: Data, result: Any, manager: DialogManager):
    if result.get('id_remainder')is not None:
        #manager.current_context().dialog_data["id_remainder"] = result["id_remainder"]
        remainder_link_to_task(result["id_remainder"], manager.current_context().dialog_data["id_task"])
    elif result.get('id_note')is not None:
        #manager.current_context().dialog_data["id_note"] = result["id_note"]
        note_link_to_task(result["id_note"], manager.current_context().dialog_data["id_task"])


async def on_end_dialog(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done({'data_task': manager.current_context().dialog_data["data_task"],
                        'id_remainder': manager.current_context().dialog_data["id_remainder"],
                        'id_note': manager.current_context().dialog_data["id_note"]})


create_task = Dialog(
    Window(
        Const('Введите название задачи'),
        MessageInput(add_to_task),
        state=TaskSG.title,
        preview_add_transitions=[Next()]
    ),
    Window(
        Const('Введите описание задачи'),
        MessageInput(add_to_task),
        state=TaskSG.description,
        preview_add_transitions=[Next()]
    ),
    Window(
        Const('Укажите дату завершения для задачи'),
        Calendar(id='calendar', on_click=on_date_selected),
        state=TaskSG.over_date,
        preview_add_transitions=[Next()]
    ),
    Window(
        Format('{data_task}'),
        Group(
            SwitchTo(Const("Хочу переписать"),
                     id='rewrite_task',
                     state=TaskSG.title),
            Button(Const('Сохранить'),
                   id='save_task',
                   on_click=save_task)
        ),
        getter=get_data,
        state=TaskSG.confirm,
        preview_add_transitions=[Cancel()]
    ),
    Window(
        Const('Вы можете создать заметку или напоминание к задаче?'),
        Group(
            Start(Const('Напоминание'),
                  id='sub_remainder',
                  state=RemainderSG.remainder_date),
            Start(Const('Заметка'),
                  id='sub_note',
                  state=NoteSG.volume),
            Button(Const('Закончить с задачей'),
                         id='end_task',
                         on_click=on_end_dialog),
        ),
        state=TaskSG.sub_r_n,
        getter=get_data,
    ),
    on_start=on_run_dialog,
    on_process_result=process_result
)
