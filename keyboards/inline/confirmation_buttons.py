from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def confirmation_keyboard(lang):
    confirm_text = {
        "en": "✅ Confirm",
        "ru": "✅ Подтвердить",
        "uz": "✅ Tasdiqlash"
    }
    cancel_text = {
        "en": "❌ Cancel",
        "ru": "❌ Отменить",
        "uz": "❌ Bekor qilish"
    }

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(confirm_text[lang], callback_data="confirm_yes"),
        InlineKeyboardButton(cancel_text[lang], callback_data="confirm_cancel")
    )
    return keyboard
