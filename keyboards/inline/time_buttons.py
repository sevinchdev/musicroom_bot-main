from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def generate_time_buttons(available_slots):
    kb = InlineKeyboardMarkup(row_width=3)
    for slot in available_slots:
        kb.insert(InlineKeyboardButton(slot, callback_data=f"time_{slot}"))
    return kb
