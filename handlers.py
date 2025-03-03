from aiogram import types
from aiogram.dispatcher.filters import Text
from bot import dp, bot
import database
import config

async def check_subscription(user_id):
    """Проверяет подписку на каналы"""
    for channel in config.CHANNELS:
        try:
            chat_member = await bot.get_chat_member(channel, user_id)
            if chat_member.status not in ["member", "administrator", "creator"]:
                return False  # Не подписан
        except:
            return False  # Ошибка проверки
    return True  # Подписан

@dp.message_handler(Text(equals="📂 Категории"))
async def show_categories(message: types.Message):
    """Показывает список категорий"""
    categories = database.get_categories()
    if not categories:
        await message.answer("Категорий пока нет.")
        return

    keyboard = types.InlineKeyboardMarkup()
    for category in categories:
        keyboard.add(types.InlineKeyboardButton(category[1], callback_data=f"category_{category[0]}"))

    await message.answer("Выбери категорию:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("category_"))
async def show_apps(callback_query: types.CallbackQuery):
    """Показывает список приложений в категории"""
    category_id = int(callback_query.data.split("_")[1])
    apps = database.get_apps_by_category(category_id)
    
    if not apps:
        await bot.send_message(callback_query.from_user.id, "В этой категории пока нет приложений.")
        return

    keyboard = types.InlineKeyboardMarkup()
    for app in apps:
        keyboard.add(types.InlineKeyboardButton(app[1], callback_data=f"app_{app[0]}"))

    await bot.send_message(callback_query.from_user.id, "Выбери приложение:", reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("app_"))
async def send_app(callback_query: types.CallbackQuery):
    """Отправляет файл после проверки подписки"""
    app_id = int(callback_query.data.split("_")[1])
    app = database.get_app_by_id(app_id)

    user_id = callback_query.from_user.id
    if not await check_subscription(user_id):
        keyboard = types.InlineKeyboardMarkup()
        for channel in config.CHANNELS:
            keyboard.add(types.InlineKeyboardButton("🔔 Подписаться", url=f"https://t.me/{channel.lstrip('@sukunafreesoft')}"))
        await bot.send_message(user_id, "Чтобы скачать приложение, подпишитесь на наши каналы!", reply_markup=keyboard)
        return

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("📖 Туториал", callback_data=f"tutorial_{app_id}"))

    await bot.send_document(user_id, app[4], caption=app[2], reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data.startswith("tutorial_"))
async def send_tutorial(callback_query: types.CallbackQuery):
    """Отправляет текстовый и видео-туториал"""
    app_id = int(callback_query.data.split("_")[1])
    app = database.get_app_by_id(app_id)

    user_id = callback_query.from_user.id

    if app[5]:  # Текстовый туториал
        await bot.send_message(user_id, app[5])

    if app[6]:  # Видео-туториал
        await bot.send_video(user_id, app[6])

@dp.message_handler(commands=['admin'])
async def admin_panel(message: types.Message):
    """Админ-панель"""
    if message.from_user.id not in config.ADMIN_IDS:
        return  

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("➕ Добавить категорию"))
    keyboard.add(types.KeyboardButton("➕ Добавить приложение"))

    await message.answer("Админ-панель:", reply_markup=keyboard)