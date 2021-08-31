from aiogram_dialog.widgets.kbd import Button, Cancel, Row, Select, ScrollingGroup
import operator
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
from base.my_requests import get_tasks, get_notes, get_task, check_completed
from base.my_requests import note_link_to_task, remainder_link_to_task


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        "task_list": dialog_manager.current_context().dialog_data.get("task_list"),
        "obj_task": dialog_manager.current_context().dialog_data.get("obj_task"),
        "list_notes": dialog_manager.current_context().dialog_data.get("list_notes"),
        "current_task": dialog_manager.current_context().dialog_data.get("current_task"),
        "list_remainders": dialog_manager.current_context().dialog_data.get("list_remainders"),
    }


async def on_end_dialog(c: CallbackQuery, button: Button, manager: DialogManager):
    await manager.done()


async def on_task_selected(c: CallbackQuery, select: Select, manager: DialogManager, item_id: int):
    manager.current_context().dialog_data["current_task"] = item_id
    manager.current_context().dialog_data["obj_task"] = get_task(item_id)
    manager.current_context().dialog_data["list_notes"] = get_notes(item_id)
    await manager.dialog().next(manager)


async def load_task_list(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().dialog_data["task_list"] = get_tasks()
    await manager.dialog().next(manager)


async def check_task_completed(c: CallbackQuery, button: Button, manager: DialogManager):
    check_completed((await get_data(manager)).get('current_task'))
    manager.current_context().dialog_data["task_list"] = get_tasks()
    await manager.dialog().back(manager)


async def process_result(start_data: Data, result: Any, manager: DialogManager):
    if result.get('id_remainder')is not None:
        remainder_link_to_task(result["id_remainder"], (await get_data(manager)).get('current_task'))
    elif result.get('id_note')is not None:
        note_link_to_task(result["id_note"], (await get_data(manager)).get('current_task'))
        manager.current_context().dialog_data["list_notes"] = get_notes((await get_data(manager)).get('current_task'))


view_task = Jinja("""
<b>{{obj_task.ftitle}}</b>
{% for v in list_notes %}
 -{{v}}
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
        Button(Const('Дальше'), id='present_list', on_click=load_task_list),
        state=MainSG.create_dialogs,
    ),
    Window(
        Const('выберите задачу'),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                id="list_task",
                item_id_getter=operator.itemgetter(1),
                items="task_list",
                on_click=on_task_selected
            ),
            id='scrl_tasks',
            width = 1,
            height = 6
        ),
        Back(Const(' Вернуться к созданию задач')),
        getter=get_data,
        state=MainSG.list_tasks
    ),
    Window(
        view_task,
        Group(
            Start(Const('Добавить заметку'), id='new_note', state=NoteSG.volume),
            Start(Const('Добавить напоминание'), id='new_remainder', state=RemainderSG.remainder_date),
            Button(Const('Отметить выполненным'), id='cheked_task', on_click=check_task_completed),
            Back(Const('Назад к списку задач')),
        ),
        parse_mode=ParseMode.HTML,
        getter=get_data,
        state=MainSG.view_present
    ),
    on_process_result=process_result
)
