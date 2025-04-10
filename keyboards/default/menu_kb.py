from aiogram.types import ReplyKeyboardMarkup, KeyboardButton




from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb(lang):
    kb = {
        'uz': ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("📅 Xona band qilish")],
                [KeyboardButton("📜 Mening rezervlarim")],
                [KeyboardButton("🤝 Tempotitanga qo'shilish")],
                [KeyboardButton("🌍 Tilni o'zgartirish")]  
            ], resize_keyboard=True
        ),
        'ru': ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("📅 Забронировать комнату")],
                [KeyboardButton("📜 Мои бронирования")],
                [KeyboardButton("🤝 Присоединиться к Tempotitan")],
                [KeyboardButton("🌍 Изменить язык")]  
            ], resize_keyboard=True
        ),
        'en': ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton("📅 Book a room")],
                [KeyboardButton("📜 My reservations")],
                [KeyboardButton("🤝 Join Tempotitan")],
                [KeyboardButton("🌍 Change Language")]  
            ], resize_keyboard=True
        )
    }

    return kb[lang]
