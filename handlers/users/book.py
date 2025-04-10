from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, ReplyKeyboardMarkup, KeyboardButton, message, InlineKeyboardMarkup, \
    InlineKeyboardButton

from db import get_connection, DB_PATH
from utils.db_api import reserve
from loader import dp
from keyboards.inline.confirmation_buttons import confirmation_keyboard
from keyboards.inline.date_buttons import generate_date_buttons
from keyboards.inline.time_buttons import generate_time_buttons
import sqlite3
from utils.db_api.user_management import get_user_language
from utils.db_api.reserve import create_table, get_user_info


# Ensure the table is created when the bot starts
create_table()

class BookingStates(StatesGroup):
    student_id = State()
    full_name = State()
    group_number = State()
    time = State()
    instrument = State()
    phone = State()
    confirmation = State()

texts = {
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
    "choose_day": {
        "en": "📆 Please select a day for reservation:",
        "ru": "📆 Пожалуйста, выберите день для бронирования:",
        "uz": "📆 Iltimos, bron qilish uchun kunni tanlang:"
    },
    "choose_time": {
        "en": "⏰ Choose available time slot:",
        "ru": "⏰ Выберите доступное время:",
        "uz": "⏰ Mavjud vaqtni tanlang:"
    },
    "enter_instrument": {
        "en": "🎶 What instrument will you play?",
        "ru": "🎶 На каком инструменте вы будете играть?",
        "uz": "🎶 Qaysi asbobda chalmoqchisiz?"
    },
    "responsibility_confirm": {
        "en": "❓ Do you confirm you’re responsible for the room? ",
        "ru": "❓ Вы подтверждаете ответственность за комнату? ",
        "uz": "❓ Xonaga javobgar ekanligingizni tasdiqlaysizmi? "
    },
    "success": {
        "en": "✅ Reservation successful!",
        "ru": "✅ Бронирование прошло успешно!",
        "uz": "✅ Bron muvaffaqiyatli bajarildi!"
    },
    "selected_day": {
        "en": "📆 Selected day:",
        "ru": "📆 Выбранный день:",
        "uz": "📆 Tanlangan kun:"
    },
    "selected_time": {
        "en": "⏰ Selected time:",
        "ru": "⏰ Выбранное время:",
        "uz": "⏰ Tanlangan vaqt:"
    },
    "reservations":{
        "en": "😕 You don't have any reservations.",
        "ru": "😕 У вас нет никаких бронирований.",
        "uz": "😕 Sizda hech qanday bronlar yo‘q."
    },
    "cancellation":{
        "en": "✅ Reservation is cancelled",
        "ru": "✅ Бронирование отменено.",
        "uz": "✅ Rezervatsiya bekor qilindi."
    },
    "no_cancellation":{
        "en": "⚠️ You can't cancel this reservation",
        "ru": "⚠️ Вы не можете отменить эту бронь.",
        "uz": "⚠️ Ushbu bronni bekor qila olmaysiz."
    },
    "cancellation_aborted":{
        "en": "✅ Reservation is not cancelled",
        "ru": "✅ Бронирование не отменено.",
        "uz": "✅ Rezervatsiya bekor qilinmadi."
    },
    "cancel_confirm":{
        "en": "❓ Do you confirm cancelling the reservation? ",
        "ru": "❓ Вы подтверждаете отмену бронирования? ",
        "uz": "❓ Rezervatsiyani bekor qilishni tasdiqlaysizmi? "
    }
}

def get_lang(user_id):
    return get_user_language(user_id)

@dp.message_handler(Text(equals=["📅 Xona band qilish", "📅 Забронировать комнату", "📅 Book a room"]))
async def start_application(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    user_data = get_user_info(message.from_user.id)

    if user_data:
        # Unpack and save existing data to FSM
        fullname, student_id, group_number, phone_number = user_data
        await state.update_data(
            fullname=fullname,
            student_id=student_id,
            group_number=group_number,
            phone_number=phone_number
        )
        # ✅ Show saved user info before proceeding
        await message.answer(
            f"👤 Full Name: {fullname}\n"
            f"🎓 Student ID: {student_id}\n"
            f"🏫 Group: {group_number}\n"
            f"📞 Phone: {phone_number}\n\n"
            + texts["enter_instrument"][lang]
        )

        await state.set_state(BookingStates.instrument)
    else:
        await message.answer(texts["full_name"][lang])
        await state.set_state(BookingStates.full_name)

@dp.message_handler(state=BookingStates.full_name)
async def get_full_name(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(fullname=message.text)
    await message.answer(texts["student_id"][lang])
    await state.set_state(BookingStates.student_id)

@dp.message_handler(state=BookingStates.student_id)
async def get_student_id(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(student_id=message.text)
    await message.answer(texts["group_number"][lang])
    await state.set_state(BookingStates.group_number)

@dp.message_handler(state=BookingStates.group_number)
async def get_group_number(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(group_number=message.text)

    contact_kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton("📲 Share Contact", request_contact=True)]],
        resize_keyboard=True, one_time_keyboard=True
    )

    await message.answer(texts["phone_number"][lang], reply_markup=contact_kb)
    await state.set_state(BookingStates.phone)

@dp.message_handler(content_types=types.ContentType.CONTACT, state=BookingStates.phone)
async def get_phone_number(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(phone_number=message.contact.phone_number)
    await message.answer(texts["enter_instrument"][lang], reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(BookingStates.instrument)

@dp.message_handler(state=BookingStates.instrument)
async def get_instrument(message: Message, state: FSMContext):
    lang = get_lang(message.from_user.id)
    await state.update_data(instrument=message.text)
    await message.answer(texts["choose_day"][lang], reply_markup=generate_date_buttons())
    # No state change here; will be set in date handler

@dp.callback_query_handler(lambda c: c.data.startswith("date_"), state=BookingStates.instrument)
async def process_date(callback_query: CallbackQuery, state: FSMContext):
    print(f"Callback received for date: {callback_query.data}")  # Debugging line
    await dp.bot.answer_callback_query(callback_query.id)
    await handle_date_selection(callback_query, state)

@dp.callback_query_handler(lambda c: c.data.startswith("time_"), state=BookingStates.time)
async def process_time(callback_query: CallbackQuery, state: FSMContext):
    await handle_time_selection(callback_query, state)

async def handle_date_selection(callback_query: CallbackQuery, state: FSMContext):
    date_str = callback_query.data.split("_")[1]
    await state.update_data(day=date_str)
    lang = get_lang(callback_query.from_user.id)

    from db import get_connection  # only once, at the top of the file

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT time FROM reservations WHERE day = ?", (date_str,))
    booked = [row[0] for row in cursor.fetchall()]

    conn.close()

    all_slots = [f"{h}:00" for h in range(9, 18)]
    available = [slot for slot in all_slots if slot not in booked]

    await callback_query.message.edit_text(f"{texts['selected_day'][lang]} {date_str}")
    await callback_query.message.answer(
        texts["choose_time"][lang], reply_markup=generate_time_buttons(available)
    )
    await BookingStates.time.set()

async def handle_time_selection(callback_query: CallbackQuery, state: FSMContext):
    time_str = callback_query.data.split("_")[1]
    await state.update_data(time=time_str, user_id=callback_query.from_user.id)
    lang = get_lang(callback_query.from_user.id)

    await callback_query.message.edit_text(f"{texts['selected_time'][lang]} {time_str}")
    data = await state.get_data()

    await callback_query.message.answer(texts["responsibility_confirm"][lang], reply_markup=confirmation_keyboard(lang))
    await BookingStates.confirmation.set()


@dp.callback_query_handler(lambda c: c.data.startswith("confirm_"), state=BookingStates.confirmation)
async def process_confirmation_callback(callback_query: CallbackQuery, state: FSMContext):
    # Update the responsibility confirmation in the state before processing
    responsibility_confirmation = callback_query.data == "confirm_yes"
    await state.update_data(responsibility_confirmation=responsibility_confirmation)

    # Pass data to handle_confirmation
    await handle_confirmation(callback_query, state)


async def handle_confirmation(callback_query: CallbackQuery, state: FSMContext):
    lang = get_lang(callback_query.from_user.id)
    await dp.bot.answer_callback_query(callback_query.id)

    # Check if the user confirmed or canceled
    if callback_query.data == "confirm_cancel":
        # Update the state with the confirmation
        await state.update_data(responsibility_confirmation="cancelled")
        await callback_query.message.edit_text("❌ Booking cancelled.")
        await state.finish()
        return

    if callback_query.data == "confirm_yes":
        # Update the state with the confirmation
        await state.update_data(responsibility_confirmation="confirmed")

    # If confirmed:
    data = await state.get_data()

    # Handle case when 'responsibility_confirmation' key might not exist
    # responsibility_confirmation = data.get('responsibility_confirmation', False)

    preview = (
        f"📋 <b>Reservation Confirmed</b>:\n\n"
        f"👤 Full Name: {data['fullname']}\n"
        f"🎓 Student ID: {data['student_id']}\n"
        f"🏫 Group: {data['group_number']}\n"
        f"📅 Date: {data['day']}\n"
        f"⏰ Time: {data['time']}\n"
        f"🎶 Instrument: {data['instrument']}\n"
        f"📞 Phone: {data['phone_number']}\n"
        f"✅ Responsibility: {data['responsibility_confirmation']}"
    )
    await callback_query.message.answer(preview, parse_mode='HTML')

    # Insert into DB
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reservations (student_id, user_id, fullname, group_number, day, time, instrument, phone_number, responsibility_confirmation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data['student_id'],
        callback_query.from_user.id,
        data['fullname'],
        data['group_number'],
        data['day'],
        data['time'],
        data['instrument'],
        data['phone_number'],
        data['responsibility_confirmation']
    ))
    conn.commit()
    conn.close()

    await callback_query.message.answer(texts["success"][lang])
    await state.finish()


# button to see reservations
@dp.message_handler(Text(equals=["📜 My reservations", "📜 Mening rezervlarim", "📜 Мои бронирования"]))
async def show_user_reservations(message: Message):
    user_id = message.from_user.id

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch reservation id (id), day, time, instrument, and responsibility_confirmation status
    cursor.execute("SELECT id, day, time, instrument, responsibility_confirmation FROM reservations WHERE user_id = ?", (user_id,))
    reservations = cursor.fetchall()


    if not reservations:
        lang = get_lang(message.from_user.id)
        await message.answer(texts["reservations"][lang])
        return

    # Loop through the fetched reservations and display them with a cancellation button
    for res in reservations:
        res_id, day, time, instrument, responsibility_confirmation = res  # Unpack 5 values (including responsibility_confirmation)

        # Check if the reservation is confirmed by the responsibility_confirmation flag
        if responsibility_confirmation == 'confirmed':  # If the responsibility is confirmed
            text = (
                f"📅 <b>Date:</b> {day}\n"
                f"⏰ <b>Time:</b> {time}\n"
                f"🎶 <b>Instrument:</b> {instrument}\n"
                f"✅ <b>Status:</b> Confirmed"
            )

            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(
                text="❌ Cancel Reservation", callback_data=f"confirm_cancel_{res_id}"
            ))

            await message.answer(text, parse_mode="HTML", reply_markup=keyboard)

    conn.close()


# Handle cancellation confirmation
@dp.callback_query_handler(lambda c: c.data.startswith("confirm_cancel_"))
async def confirm_cancellation(callback_query: CallbackQuery):
    res_id = int(callback_query.data.split("_")[2])  # Extract reservation ID
    user_id = callback_query.from_user.id  # User who is requesting the cancellation

    # Ask for confirmation from the user (Yes/No)
    lang = get_lang(callback_query.from_user.id)
    confirmation_text = texts["cancel_confirm"][lang]  # The confirmation prompt
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="✅ Yes", callback_data=f"cancel_{res_id}"),
        InlineKeyboardButton(text="❌ No", callback_data=f"no_cancel_{res_id}")
    )

    await callback_query.message.edit_text(confirmation_text, reply_markup=keyboard)


# Process the cancellation (if confirmed)
@dp.callback_query_handler(lambda c: c.data.startswith("cancel_"))
async def cancel_reservation(callback_query: CallbackQuery):
    res_id = int(callback_query.data.split("_")[1])  # Reservation ID
    user_id = callback_query.from_user.id  # User ID requesting the cancellation

    conn = get_connection()
    cursor = conn.cursor()

    # Double-check if the user owns the reservation
    cursor.execute("SELECT user_id FROM reservations WHERE id = ?", (res_id,))
    row = cursor.fetchone()

    if row and row[0] == user_id:
        cursor.execute("DELETE FROM reservations WHERE id = ?", (res_id,))
        conn.commit()

        # Send confirmation of cancellation
        lang = get_lang(callback_query.from_user.id)
        await callback_query.message.edit_text(texts["cancellation"][lang])  # Confirmation message
    else:
        lang = get_lang(callback_query.from_user.id)
        await callback_query.message.answer(texts["no_cancellation"][lang])  # Error message if not the owner

    conn.close()


# Handle cancellation cancellation (if user selects "No")
@dp.callback_query_handler(lambda c: c.data.startswith("no_cancel_"))
async def no_cancel_reservation(callback_query: CallbackQuery):
    lang = get_lang(callback_query.from_user.id)
    await callback_query.message.edit_text(texts["cancellation_aborted"][lang])  # Cancellation was aborted
