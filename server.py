""" Server of Telegram bot we are running """

import logging
import os

from aiogram import Dispatcher, Bot, executor, types
from middlewares import AccessMiddleware


logging.basicConfig(level=logging.INFO)
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
ACCESS_ID = os.getenv('TELEGRAM_ACCESS_ID')

bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))

@dp.message_handler(commands=['start', 'help'])
async def welcome_handler(message: types.Message) -> None:
    logging.info(f'User {message.from_user} connected')
    # Welcome message
    await message.answer("Бот ведення персональних витрат:\n\n"
        "Додати витрати: 120 харчі\n"
        "Витрати за сьогодні: /today\n"
        "Витрати за поточний місяць: /month\n"
        "Останні витрати: /expenses\n"
        "Категорії: /categories")


if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
