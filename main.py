import sys
from database.common.models import History, db
import asyncio
import logging
from database.core import crud
from aiogram import Bot, Dispatcher, F, Router
from TG_API.core.utils.commands import set_commands
from TG_API.core.handlers.basic import get_inline, get_start, command_start, get_period, get_summary, cancel_handler
from TG_API.core.handlers.callback import get_weather
from aiogram.filters import Command
from settings import TelegramSettings
from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    city = State()
    days = State()
    
    
db_write = crud.create()
db_read = crud.retrieve()

form_router = Router()

# db_write(db, History, data)

# retrieved = db_read(db, History, History.city, History.message)
#
# for element in retrieved:
#     print(element.number, element.message)


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(TelegramSettings.TG_admin_id, text='Bot started')


async def stop_bot(bot: Bot):
    await bot.send_message(TelegramSettings.TG_admin_id, text='Bot stopped')


async def main():
    bot = Bot(token=TelegramSettings.TG_api_key, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(form_router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_inline, Command(commands=['inline']))
    dp.message.register(get_start, Command(commands=['start']))
    dp.message.register(command_start, Command(commands=['start', 'weather']))
    dp.message.register(get_period, Form.city)
    dp.message.register(get_summary, Form.days)
    dp.message.register(cancel_handler, F.cancel, Command(commands=['cancel']))
    dp.callback_query.register(get_weather)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())