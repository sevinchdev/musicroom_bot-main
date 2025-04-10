from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from loader import bot
from utils.db_api.user_management import is_user_blocked
from utils.db_api.channel_management import get_channels



class CheckSubscribeMiddleware(BaseMiddleware):
    async def on_process_update(self, update: types.Update, data: dict):
        not_subscribed_channels = []
        user_id = ((update['message']['from']['id'] if 'message' in update 
                    else update['callback_query']['from']['id']
                    ) if 'message' in update or 'callback_query' in update else 0)

        if is_user_blocked(user_id):
            message = "❌ <b>Admin tomonidan botdan bloklangansiz. Blokni ochish uchun admin bilan bog'laning!</b>"
            if 'message' in update:
                await update.message.answer(message)
            elif 'callback_query' in update:
                await update.callback_query.message.answer(message)
            raise CancelHandler() 

        for channel in get_channels():
            channel = int(channel[0])
            chat_member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if chat_member['status'] == 'left':
                not_subscribed_channels.append(channel)

        if not_subscribed_channels:
            kb_list = [
                [
                    types.InlineKeyboardButton(
                        text=(await bot.get_chat(chat_id=channel)).full_name,
                        url=(await bot.get_chat(chat_id=channel)).invite_link
                    )
                ] for channel in not_subscribed_channels
            ]
            kb_list.append([types.InlineKeyboardButton(text="Tasdiqlash ✅", callback_data='check_subscribe')])
            kb = types.InlineKeyboardMarkup(inline_keyboard=kb_list)
            message = f"""Botdan foydalanish uchun 
pastdagi <b>KANALLARGA</b> obuna bo'ling!
"""
            await ((update.message.answer(message, reply_markup=kb)) if 'message' in update else (update.callback_query.message.answer(message, reply_markup=kb)))
            raise CancelHandler()