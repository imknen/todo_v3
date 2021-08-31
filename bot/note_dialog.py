from aiogram_dialog.widgets.kbd import Button, Cancel
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Back, Next
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import Message, CallbackQuery
from .states_dialog import NoteSG
from base.my_requests import save_note

async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        "fvolume": dialog_manager.current_context().dialog_data.get("fvolume")
    }


async def save_data(m: Message, dialog: Dialog, manager: DialogManager):
    manager.current_context().dialog_data["fvolume"] = m.text
    manager.current_context().dialog_data["id_note"] = save_note(await get_data(manager))
    await manager.done({'id_note': manager.current_context().dialog_data["id_note"]})


create_note = Dialog(
    Window(
        Const('Введите данные для заметки.'),
        MessageInput(save_data),
        state=NoteSG.volume,
        preview_add_transitions=[Cancel()]
    ),
)
