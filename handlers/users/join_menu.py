from aiogram import types
from loader import dp , bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from data.config import ADMINS
from keyboards.default.menu_kb import main_menu_kb
from utils.db_api.user_management import get_user_language

class TempotitanForm(StatesGroup):
    full_name = State()
    student_id = State()
    group_number = State()
    phone_number = State()
    instrument = State()
    about = State()
    confirmation = State()


messages = {
    "full_name": {
        "uz": "📛 Iltimos, to'liq ismingizni kiriting:",
        "ru": "📛 Пожалуйста, введите ваше полное имя:",
        "en": "📛 Please enter your full name:"
    },
    "student_id": {
        "uz": "🎓 Universitet student ID raqamingizni kiriting:",
        "ru": "🎓 Введите ваш студенческий ID:",
        "en": "🎓 Enter your university student ID:"
    },
    "group_number": {
        "uz": "🏫 Universitet guruh raqamingizni kiriting:",
        "ru": "🏫 Введите номер вашей группы в университете:",
        "en": "🏫 Enter your university group number:"
    },
    "phone_number": {
        "uz": "📞 Telefon raqamingizni ulashing:",
        "ru": "📞 Поделитесь своим номером телефона:",
        "en": "📞 Share your phone number:"
    },
    "instrument": {
        "uz": "🎸 Qaysi musiqa asbobini chalishni bilasiz?",
        "ru": "🎸 Какой музыкальный инструмент вы играете?",
        "en": "🎸 What instrument do you play?"
    },
    "about": {
        "uz": "📖 O'zingiz haqingizda qisqacha yozing:",
        "ru": "📖 Напишите немного о себе:",
        "en": "📖 Write a short description about yourself:"
    },
    "confirmation": {
        "uz": "✅ Agar ma'lumotlar to'g'ri bo'lsa, 'Tasdiqlash' tugmasini bosing.",
        "ru": "✅ Если данные верны, нажмите 'Подтвердить'.",
        "en": "✅ If the information is correct, press 'Confirm'."
    },
    "application_sent": {
        "uz": "✅ Arizangiz adminlarga yuborildi! Javob kuting.",
        "ru": "✅ Ваша заявка отправлена администраторам! Ожидайте ответа.",
        "en": "✅ Your application has been sent to the admins! Please wait for a response."
    },
    "application_canceled": {
        "uz": "❌ Ariza bekor qilindi.",
        "ru": "❌ Заявка отменена.",
        "en": "❌ Application canceled."
    }
}


def get_lang(user_id):
    return get_user_language(user_id) 


@dp.message_handler(Text(equals=["🤝 Tempotitanga qo'shilish", "🤝 Присоединиться к Tempotitan", "🤝 Join Tempotitan"]))
async def start_application(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await message.answer(messages["full_name"][lang])
    await state.set_state(TempotitanForm.full_name)


@dp.message_handler(state=TempotitanForm.full_name)
async def get_full_name(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(full_name=message.text)
    await message.answer(messages["student_id"][lang])
    await state.set_state(TempotitanForm.student_id)


@dp.message_handler(state=TempotitanForm.student_id)
async def get_student_id(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(student_id=message.text)
    await message.answer(messages["group_number"][lang])
    await state.set_state(TempotitanForm.group_number)


@dp.message_handler(state=TempotitanForm.group_number)
async def get_group_number(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(group_number=message.text)

    contact_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("📲 Share Contact", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )

    await message.answer(messages["phone_number"][lang], reply_markup=contact_kb)
    await state.set_state(TempotitanForm.phone_number)


@dp.message_handler(content_types=types.ContentType.CONTACT, state=TempotitanForm.phone_number)
async def get_phone_number(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(phone_number=message.contact.phone_number)
    await message.answer(messages["instrument"][lang])
    await state.set_state(TempotitanForm.instrument)


@dp.message_handler(state=TempotitanForm.instrument)
async def get_instrument(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(instrument=message.text)
    await message.answer(messages["about"][lang])
    await state.set_state(TempotitanForm.about)

@dp.message_handler(state=TempotitanForm.about)
async def get_about_text(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(about=message.text)

    user_data = await state.get_data()
    confirmation_text = (
        f"📋 <b>Application Summary:</b>\n\n"
        f"👤 <b>Name:</b> {user_data['full_name']}\n"
        f"🎓 <b>Student ID:</b> {user_data['student_id']}\n"
        f"🏫 <b>Group Number:</b> {user_data['group_number']}\n"
        f"📞 <b>Phone:</b> {user_data['phone_number']}\n"
        f"🎸 <b>Instrument:</b> {user_data['instrument']}\n"
        f"📝 <b>About:</b> {user_data['about']}\n\n"
    )

    confirm_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("✅ Confirm"), KeyboardButton("❌ Cancel")]],
        resize_keyboard=True, one_time_keyboard=True
    )

    await message.answer(confirmation_text, reply_markup=confirm_kb, parse_mode="HTML")
    await state.set_state(TempotitanForm.confirmation)


@dp.message_handler(lambda message: message.text in ["✅ Confirm", "❌ Cancel"], state=TempotitanForm.confirmation)
async def confirm_application(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    
    if message.text == "✅ Confirm":
        user_data = await state.get_data()

        username = message.from_user.username
        if username:
            username_text = f"📎 <b>Username:</b> @{username}"
        else:
            username_text = f"📎 <b>Profile:</b> <a href='tg://user?id={message.from_user.id}'>Click Here</a>"

        admin_message = (
            "📢 <b>New Application joining TEMPOTITANS!</b>\n\n"
            f"👤 <b>Name:</b> {user_data['full_name']}\n"
            f"🎓 <b>Student ID:</b> {user_data['student_id']}\n"
            f"🏫 <b>Group:</b> {user_data['group_number']}\n"
            f"📞 <b>Phone:</b> {user_data['phone_number']}\n"
            f"🎸 <b>Instrument:</b> {user_data['instrument']}\n"
            f"📝 <b>About:</b> {user_data['about']}\n"
            f"{username_text}\n\n"
            "📩 Please review this application."
        )

        for ADMIN_ID in ADMINS:
            await bot.send_message(int(ADMIN_ID), admin_message, parse_mode="HTML")
            
        await message.answer(messages["application_sent"][lang], reply_markup=main_menu_kb(lang))
    else:
        await message.answer(messages["application_canceled"][lang], reply_markup=main_menu_kb(lang))

    await state.finish()