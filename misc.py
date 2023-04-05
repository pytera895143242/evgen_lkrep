import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = '6142426452:AAGl5LwlNcdSnl41hXekMsANyKmyk4gxPgw'
memory_storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode='html')
dp = Dispatcher(bot,storage=memory_storage)
logging.basicConfig(level=logging.INFO)