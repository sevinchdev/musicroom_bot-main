from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

lang_btn = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿O'zbekcha", callback_data="lang_uz"),InlineKeyboardButton(text="🇷🇺Russian", callback_data="lang_ru"),InlineKeyboardButton(text="🇺🇸English", callback_data="lang_en")]
    ]
)

lang_btn_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿O'zbekcha", callback_data="settings_lang_uz"),InlineKeyboardButton(text="🇷🇺Russian", callback_data="settings_lang_ru"),InlineKeyboardButton(text="🇺🇸English", callback_data="settings_lang_en")]
    ]
)