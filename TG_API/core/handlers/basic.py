from aiogram.types import Message
import json
import logging
from typing import Any, Dict
from aiogram import Bot, Router, html
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from site_API.core import site_api, url, headers
from TG_API.core.keyboards.reply import get_reply_keyboard
from TG_API.core.keyboards.inline import get_inline_keyboard
from aiogram.types import ReplyKeyboardRemove

form_router = Router()

method = "GET"
timeout = 15


class Form(StatesGroup):
    city = State()
    days = State()


storage = MemoryStorage()


async def command_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.city)
    await message.answer(
        "Давайте уточним, напишите название города"
    )


async def get_period(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await state.set_state(Form.days)
    await message.answer('За какой период(в днях)?')


async def get_summary(message: Message, state: FSMContext) -> None:
    await state.update_data(days=message.text)
    data = await state.get_data()
    await state.clear()
    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any]) -> None:
    city: str = str(data["city"])
    days: str = str(data["days"])
    params = {"days": days, "q": city}
    text = f"И так город: {html.quote(city)}, период: {html.quote(days)} дней"
    await message.answer(text=text)
    response = site_api.get_forecast_weather(method, url, headers, params=params, timeout=timeout)
    response = response.json()
    await message.answer('Вот что я нашел: ', parse_mode='HTML')
    for i_weather in range(0, int(days)):
        response_sunrise = response['forecast']['forecastday'][i_weather]['astro']['sunrise']
        response_sunset = response['forecast']['forecastday'][i_weather]['astro']['sunset']
        response_data = response['forecast']['forecastday'][i_weather]['hour'][0]['time']
        response_temp = response['forecast']['forecastday'][i_weather]['hour'][0]['temp_c']
        await message.answer(f'\nДата: {response_data}, \nТемпература по С: {response_temp}, '
                             f'\nВосход солнца {response_sunrise}, \nЗакат {response_sunset}', parse_mode='HTML')


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
    

async def get_inline(message: Message):
    await message.answer(f'Привет, <tg-spoiler>{message.from_user.first_name}</tg-spoiler>. Меня зовут Знайка. Вот что я умею: ->',
                         reply_markup=get_inline_keyboard())


async def get_start(message: Message):
    await message.answer(f'<tg-spoiler>Hello, '
                        f'{message.from_user.first_name}</tg-spoiler>',
                        reply_markup=get_reply_keyboard())


async def get_location(message: Message):
    await message.answer(
        f'You send location: \r\a<tg-spoiler>{message.location.latitude}</tg-spoiler>\r\n<tg-spoiler>{message.location.longitude}</tg-spoiler>')


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'<b>Great! Its a picture</b>. I will save it')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'saved_images/photo.jpg')
    