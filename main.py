import logging
import asyncio
from aiogram_dialog import DialogRegistry
from aiogram import Bot, Dispatcher, executor
from aiogram_dialog.tools import render_transitions
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from bot.task_dialog import create_task
from bot.remainder_dialog import create_remainder
from bot.note_dialog import create_note
from bot.main_dialog import main_dialog
from bot.states_dialog import TaskSG, MainSG, NoteSG
from config.config_reader import load_config

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Запуск todo"),
        #BotCommand(command='/newtask', description='Новая задача'),
        #BotCommand(command="/test", description="тест"),
    ]
    await bot.set_my_commands(commands)


render_transitions([create_task, create_remainder, create_note, main_dialog])

async def main():
    # Настройка логирования в stdout
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    # Парсинг файла конфигурации
    config = load_config("config/bot.ini")

    # Объявление и инициализация объектов бота и диспетчера
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    registry = DialogRegistry(dp)
    registry.register_start_handler(MainSG.create_dialogs)  # resets stack and start dialogs on /start command
    registry.register(main_dialog)
    registry.register(create_task)
    registry.register(create_remainder)
    registry.register(create_note)
    render_transitions(registry)  # render , MainSGraph with current transtions


    # Установка команд бота
    await set_commands(bot)

    await dp.skip_updates()
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
