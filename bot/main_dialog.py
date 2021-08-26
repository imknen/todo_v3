from aiogram_dialog.widgets.kbd import Button, Cancel, Row
from aiogram_dialog.widgets.text import Const, Format, Case, Multi
from aiogram_dialog.widgets.kbd import Back, Cancel, Start, Next, Group, SwitchTo
from aiogram_dialog import Dialog, DialogManager, Window, DialogRegistry, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message, CallbackQuery
from typing import Any
from datetime import date, datetime
from aiogram.types import ParseMode
from aiogram_dialog.widgets.text import Jinja
from .states_dialog import TaskSG, RemainderSG, MainSG, NoteSG
from base.my_requests import get_tasks


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        "task_list": dialog_manager.current_context().dialog_data.get("task_list"),
        "size_list": dialog_manager.current_context().dialog_data.get("size_list"),
        "counter": dialog_manager.current_context().dialog_data.get("counter")
    }


async def check_prev(c: CallbackQuery, button: Button, manager: DialogManager):
    if manager.current_context().dialog_data["counter"] != 0:
        manager.current_context().dialog_data["counter"] -= 1


async def check_next(c: CallbackQuery, button: Button, manager: DialogManager):
    if manager.current_context().dialog_data["counter"] != (await get_data(manager)).get('size_list'):
        manager.current_context().dialog_data["counter"] += 1


async def on_end_dialog(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()


async def get_task_list(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().dialog_data["task_list"] = get_tasks()
    manager.current_context().dialog_data['counter'] = 0
    manager.current_context().dialog_data["size_list"] = len((await get_data(manager)).get('task_list')) -1
    await manager.dialog().next(manager)

async def select_item(c: CallbackQuery, button: Button, manager: DialogManager):
    pass


html_text = Jinja("""
<b>Список задач</b>
{% for k,v in task_list.items() %}
{% if k == counter %}=>{% else %}  {% endif %}{{v.ftitle}}
{% endfor %}
""")


main_dialog = Dialog(
    Window(
        Const("Планировщик ваших задач"),
        Group(
            Start(Const("Создать задачу"), id="new_task", state=TaskSG.title),
            Start(Const("Создать напоминание"), id='new_remainder', state=RemainderSG.remainder_date),
            Start(Const("Создать заметку"), id='new_note', state=NoteSG.volume)
        ),
        Button(Const('Дальше'), id='present_list', on_click=get_task_list),
        state=MainSG.create_dialogs,
    ),
    Window(
        html_text,
        Back(Const('Хочу что то запланировать')),
        Row(
            Button(Const('<<'), id='prev', on_click=check_prev),
            Button(Const('*'), id='select', on_click=select_item),
            Button(Const('>>'), id='next', on_click=check_next),
        ),
        Next(Const('Дальше')),
        parse_mode=ParseMode.HTML,
        getter=get_data,
        state=MainSG.list_tasks
    ),
)
