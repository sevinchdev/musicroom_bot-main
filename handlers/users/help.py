from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from filters.admin import is_admin


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/help - Yordam")
    if is_admin(message.from_user.id):
        text = (
            "Menyular haqida:",
            "<b>📤Foydalanuvchilarga xabar yuborish</b>: Foydalanuvchilarga qandaydir reklama yoki xabar yuborish uchun ishlatiladi",
            "<b>📊 Statistika</b>: Botda nechta aktiv foydalanuvchilar borligi haqida malumot beradi",
            "<b>➕Kino qo'shish</b>: Botga kino qo'shish",
            "<b>🗑Kino o'chirish</b>: Botdan kinoni o'chirib beradi",
            "<b>➕Kanal qo'shish</b>: Botga majburiy obuna uchun kanal qo'shish",            
            "<b>🗑Kanal o'chirish</b>: Botdan majburiy obunadagi kerakli kanalni o'chirib beradi",     
            "<b>🧹Botni tozalash</b>: Botdagi barcha kino va kanallarni o'chirib tashlaydi",
            "<b>/toggle_block ID </b>: Foydalanuvchini bloklash va blokdan ochish(Masalan:/toggle_block 1234567)"  
        )
        await message.answer("\n\n".join(text))
    else:
        await message.answer("\n".join(text))
