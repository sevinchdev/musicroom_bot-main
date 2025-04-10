from aiogram import types
from loader import dp , bot
from utils.db_api.user_management import add_user
from keyboards.inline.inlines import lang_btn,lang_btn_settings
from keyboards.default.menu_kb import main_menu_kb



@dp.message_handler(lambda message: message.text in ["🌍 Tilni o'zgartirish","🌍 Изменить язык",'🌍 Change Language'])
async def change_language(message:types.Message):
    await message.answer("<b>Choose language</b>", reply_markup=lang_btn_settings)


@dp.callback_query_handler(lambda call: call.data.startswith("settings_lang"))
async def add_user_db(call: types.CallbackQuery):
    lang = call.data.split("_")[2]
    user_lang = lang if lang in ["uz", "ru", "en"] else "ru"  

    add_user(call.from_user.id, call.from_user.username, call.from_user.full_name, user_lang)

    confirmation_msg = {
        "uz": "✅ Til o'zgartirildi: O'zbek tili",
        "ru": "✅ Язык изменен: Русский",
        "en": "✅ Language changed to: English"
    }
    msg2 = {
        'uz': "Bosh menyu",
        'ru': "Главное меню",
        'en': "Main menu"
    }
    await call.message.edit_text(confirmation_msg[lang])
    await bot.send_message(
        chat_id=call.from_user.id,
        text=msg2[lang],
        reply_markup=main_menu_kb(lang)
    )

