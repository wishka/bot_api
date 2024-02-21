import sys
from site_API.core import site_api, url, headers
from database.common.models import History, db
import asyncio
import logging
from typing import Any, Dict
from database.core import crud
from TG_API.utils.tg_api_handler import bot
from TG_API.utils.tg_api_handler import TelegramInterface
from aiogram import Bot, Dispatcher, types, F, Router, html
from TG_API.core.handlers.basic import get_photo, get_hello
from TG_API.core.handlers.basic import get_start
from TG_API.core.utils.commands import set_commands
from TG_API.core.handlers.basic import get_location, start_get_weather
from TG_API.core.handlers.basic import get_inline
from TG_API.core.handlers.callback import select_macbook, get_weather, days_count
from aiogram.types import (ContentType, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.filters import Command, CommandStart
from TG_API.core.settings import settings
from TG_API.core.utils.callbackdata import MacInfo
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

db_write = crud.create()
db_read = crud.retrieve()

form_router = Router()

method = "GET"
timeout = 15


class Form(StatesGroup):
    city = State()
    days = State()
    language = State()


storage = MemoryStorage()

# db_write(db, History, data)

# retrieved = db_read(db, History, History.city, History.message)
#
# for element in retrieved:
#     print(element.number, element.message)


@form_router.message(Command('weather'))
async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.city)
    await message.answer(
        "Давайте уточним, напишите название города"
    )


@form_router.message(Form.city)
async def process_city(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await state.set_state(Form.days)
    await message.answer('За какой период(в днях)?')


@form_router.message(Form.days)
async def process_like_write_bots(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    await state.clear()
    await show_summary(message=message, data=data)


@form_router.message(Form.days)
async def process_unknown_write_bots(message: Message) -> None:
    await message.reply("I don't understand you :(")


# @form_router.message(Form.language)
# async def process_language(message: Message, state: FSMContext) -> None:
#     data = await state.update_data(language=message.text)
#     await state.clear()
#
#     if message.text.casefold() == "python":
#         await message.reply(
#             "Python, you say? That's the language that makes my circuits light up! 😉"
#         )
#
#     await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any]) -> None:
    
    city = data["city"]
    days = data["days"]
    params = {"days": days, "q": city}
    text = f"И так город: {html.quote(city)}, период: {html.quote(days)} дней"
    await message.answer(text=text)
    response = site_api.get_forecast_weather(method, url, headers, params=params, timeout=timeout)
    response = response.json()
    print(response)
    response_set = response['forecast']['forecastday'][2]['astro']
    print(response_set)
    await message.answer('Вот что я нашел: ', response_set, parse_mode='html')
    


@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=ReplyKeyboardRemove(),
    )


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Bot started')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Bot stopped')


# async def start():
#     bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
#     dp = Dispatcher()
#     logging.basicConfig(level=logging.INFO)
#
    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)
#     dp.message.register(get_location, F.location)
#     # dp.message.register(get_start)
#     dp.message.register(start_get_weather, Command(commands=['weather']))
#     dp.message.register(get_inline, Command(commands=['inline']))
#     # Так как мы обрабатываем апдейт на callbackquery событие то обращаемся к диспетчеру через callback query
#     dp.callback_query.register(select_macbook, MacInfo.filter())
#     dp.message.register(get_photo, F.photo)
#     dp.callback_query.register(get_weather)
#     # dp.message.register(days_count)
#     # dp.message.register(get_hello, F.text == 'Hello')
#
#     try:
#         await dp.start_polling(bot)
#     finally:
#         await bot.session.close()


# if __name__ == '__main__':
#     asyncio.run(start())
    
# TelegramInterface()

# bot.polling(none_stop=True)

async def main():
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()
    dp.include_router(form_router)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_inline, Command(commands=['inline']))
    # dp.message.register(get_start)
    dp.callback_query.register(get_weather)
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())