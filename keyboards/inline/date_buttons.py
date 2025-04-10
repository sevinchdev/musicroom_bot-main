from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta


def generate_date_buttons(days_ahead=5):
    keyboard = InlineKeyboardMarkup(row_width=2)
    today = datetime.today()

    added = 0
    day = today + timedelta(days=1)
    while added < days_ahead:
        if day.weekday() != 6:  # Skip Sunday
            date_str = day.strftime('%Y-%m-%d')
            label = day.strftime('%A %d-%b')
            keyboard.insert(InlineKeyboardButton(label, callback_data=f"date_{date_str}"))
            added += 1
        day += timedelta(days=1)

    return keyboard
