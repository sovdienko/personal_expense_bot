""" Server of Telegram bot we are running """
import logging
import os

from aiogram import Dispatcher, Bot, executor, types
from middlewares import AccessMiddleware
import expenses
import exceptions
from categories import Categories


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


@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """видаляємо витрати"""
    row_id = int(message.text[4:])
    expenses.delete_expense(row_id)
    await message.answer('Видалено')

@dp.message_handler(commands=['categories'])
async def categories_list(message: types.Message):
    """Send list of Expense Categories"""
    categories = Categories().get_all_categories()
    await message.answer("Категоріі витрат: \n\n* " + \
                         ("\n* ".join([c.name+' ('+', '.join(c.aliases)+')' for c in categories])))


@dp.message_handler(commands=['today'])
async def today_statistic(message: types.Message):
    """Send today's statistic of Expenses"""
    await message.answer(expenses.get_today_statistic())


@dp.message_handler(commands=['month'])
async def month_statistic(message: types.Message):
    """Send current month statistic of Expenses"""
    await message.answer(expenses.get_month_statistic())


@dp.message_handler(commands=['expenses'])
async def list_expenses(message: types.Message):
    """Send the last Expenses"""
    last_expenses = expenses.last()
    if not last_expenses:
        await message.answer("Витрати відсутні")
        return

    last_expenses_rows = [
        f"{expense.amount} грн. на {expense.category_name} - натисни " 
        f"/del{expense.id} щоб видалити"
        for expense in last_expenses]

    await message.answer("Останні збережені витрати:\n\n* " +
                         "\n\n* ".join(last_expenses_rows))


@dp.message_handler()
async def add_expense(message: types.Message):
    """Додаємо нові витрати"""
    try:
        expense = expenses.add_expense(message.text)
    except exceptions.NotCorrectMessage as e:
        await message.answer(str(e))
        return
    await message.answer(
        f"Додані витрати {expense.amount} грн. на {expense.category_name}.\n\n"
        f"{expenses.get_today_statistic()}")



if __name__ == '__main__':
    executor.start_polling(dispatcher=dp, skip_updates=True)
