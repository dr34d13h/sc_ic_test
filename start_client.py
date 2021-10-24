from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN_CLIENT
from keyboard import welcome_keyboard
import create_event, catalogue_event, contact_event


storage = MemoryStorage()
bot = Bot(token=TOKEN_CLIENT)
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':

    create_event.register_handlers_client(dp, bot)
    catalogue_event.register_handlers_client(dp, bot)
    contact_event.register_handlers_client(dp, bot)    

    executor.start_polling(dp, skip_updates=True)
