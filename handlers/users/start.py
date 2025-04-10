from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from utils.db_api.user_management import get_user_language, add_user, update_user_contact
from keyboards.inline.inlines import lang_btn
from aiogram.dispatcher import FSMContext
from filters.admin import is_admin
from keyboards.default.menu_kb import main_menu_kb

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext): 
    lang = get_user_language(message.from_user.id)
    if lang:
        msg2 = {
            'uz': "Bosh menyu",
            'ru': "Главное меню",
            'en': "Main menu"
        }

        await message.answer(
            text=msg2[lang],
            reply_markup=main_menu_kb(lang)
        )
    else:
        await message.answer("<b>Choose language</b>", reply_markup=lang_btn)

@dp.callback_query_handler(lambda call: call.data.startswith("lang"))
async def add_user_db(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    user_lang = lang if lang in ["uz", "ru", "en"] else "ru"  

    add_user(call.from_user.id, call.from_user.username, call.from_user.full_name, user_lang)

    confirmation_msg = {
        "uz": "✅ Til o'zgartirildi: O'zbek tili",
        "ru": "✅ Язык изменен: Русский",
        "en": "✅ Language changed to: English"
    }
    await call.message.edit_text(confirmation_msg[lang])

    contact_request_msg = {
        "uz": "📞 Iltimos, telefon raqamingizni yuboring.",
        "ru": "📞 Пожалуйста, отправьте свой номер телефона.",
        "en": "📞 Please send your phone number."
    }

    contact_kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton("📲 Share Contact", request_contact=True)]
        ], resize_keyboard=True, one_time_keyboard=True
    )

    await bot.send_message(
        chat_id=call.from_user.id,
        text=contact_request_msg[lang],
        reply_markup=contact_kb
    )


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def receive_contact(message: types.Message):
    user_id = message.from_user.id
    phone_number = message.contact.phone_number

    update_user_contact(user_id, phone_number)

    confirmation_msg = {
        "uz": "✅ Telefon raqamingiz saqlandi!",
        "ru": "✅ Ваш номер телефона сохранен!",
        "en": "✅ Your phone number has been saved!"
    }


    msg2 = {
        'uz': "Bosh menyu",
        'ru': "Главное меню",
        'en': "Main menu"
    }
    lang = get_user_language(user_id) 
    await message.answer(confirmation_msg[lang], reply_markup=main_menu_kb(lang))

    await message.answer(
        text=msg2[lang],
        reply_markup=main_menu_kb(lang)
    )