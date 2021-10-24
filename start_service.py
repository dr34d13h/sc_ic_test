from aiogram import Bot, types, executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import service
from config import TOKEN_SERVICE


storage = MemoryStorage()
bot = Bot(token=TOKEN_SERVICE)
dp = Dispatcher(bot, storage=storage)


if __name__ == '__main__':
    service.register_handlers_client(dp, bot)
    executor.start_polling(dp, skip_updates=True)
