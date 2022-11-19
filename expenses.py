import datetime
import re
from typing import NamedTuple, List, Optional

import pytz

import exceptions
import db
from categories import Categories


class Message(NamedTuple):
    """Parsed message structure of new expense"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """New Expense structure added into DB"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    """Add a new expense based on the typed message"""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)
    db.insert('expense', {
        'amount': parsed_message.amount,
        'created': _get_now_formatted(),
        'category_codename': category.codename,
        'raw_text': raw_message
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def delete_expense(row_id: int) -> None:
    """Delete expense by its ID"""
    db.delete('expense', row_id)


def get_today_statistic() -> str:
    """Returns today's statistic in text format"""
    cursor = db.get_cursor()
    cursor.execute("select sum(amount) "
                   "from expense "
                   "where date(created) = date ('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Витрати за сьогодні відсутні"
    all_today_expenses = result[0]
    cursor.execute("select sum(amount) "
                   "from expense "
                   "where date(created) = date ('now', 'localtime') "
                   " and category_codename in (select codename "
                   "from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    return (f"Витрати сьогодні:\n"
            f" усього - {all_today_expenses} грн.\n"
            f" базові - {base_today_expenses} грн. з {_get_budget_limit()} грн.\n"
            f"За поточний місяць: /month")


def get_month_statistic() -> str:
    """Returns current month statistic in text format"""
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) "
                   f"from expense "
                   f"where date(created) >= {first_day_of_month}")
    result = cursor.fetchone()
    if not result[0]:
        return "Витрати за поточний місяць відсутні"
    all_month_expenses = result[0]
    cursor.execute(f"select sum(amount) "
                   f"from expense "
                   f"where date(created) >= {first_day_of_month} "
                   f" and category_codename in (select codename "
                   f"from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_month_expenses = result[0] if result[0] else 0
    return (f"Витрати у поточному місяці:\n"
            f" усього - {all_month_expenses} грн.\n"
            f" базові - {base_month_expenses} грн. з {now.day * _get_budget_limit()} грн.\n"
            f"За поточний місяць: /month")


def last() -> List[Expense]:
    """Returns the last Expenses"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name "
        "from expense e left join category c "
        "on c.codename = e.category_codename "
        "order by created desc limit 10")
    rows = cursor.fetchall()
    last_expenses = [Expense(id=row[0],
                             amount=row[1],
                             category_name=row[2]) for row in rows]
    return last_expenses


def _parse_message(raw_message: str) -> Message:
    """Parsing typed message for new Expense creation"""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не можу розібрати вхідне повідомлення. "
            "Очікуємий формат, наприклад:\n"
            " 2000 одяг")

    amount = int(regexp_result.group(1).replace(" ", ""))
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_budget_limit() -> int:
    """Returns day budget limit for basic expenses"""
    return int(db.fetchall('budget', ['daily_limit'])[0]['daily_limit'])


def _get_now_formatted() -> str:
    """Returns today's date in the String format"""
    return _get_now_datetime().strftime('%Y-%m-%d %H:%M:%S')


def _get_now_datetime() -> datetime.datetime:
    """Returns today's datetime for Kyiv timezone"""
    tz = pytz.timezone('Europe/Kyiv')
    return datetime.datetime.now(tz)
