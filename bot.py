from unicodedata import name
from aiogram import Bot, Dispatcher, types # type: ignore
from aiogram.utils import executor # type: ignore
import config
import database
import handlers

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("📂 Категории"))
    await message.answer("Привет! Выбери категорию:", reply_markup=keyboard)

if name == 'main':
    database.init_db()  # Создаём базу при запуске
    executor.start_polling(dp)