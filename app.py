from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.db_api.create import create_table
from middlewares.channel import CheckSubscribeMiddleware

async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    dispatcher.middleware.setup(CheckSubscribeMiddleware())
    await on_startup_notify(dispatcher)
    create_table()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)


