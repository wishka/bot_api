from aiogram import Bot
import asyncio
from typing import Any, Dict
from aiogram.types import CallbackQuery
from TG_API.core.utils.callbackdata import MacInfo
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types, html
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (ContentType, KeyboardButton, Message, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from aiogram.enums import ParseMode


# States
class Form(StatesGroup):
    city = State()  # Will be represented in storage as 'Form:name'
    days = State()  # Will be represented in storage as 'Form:age'
    
    
storage = MemoryStorage()
    
questions = ["Напишите название города", "За какой период(в днях)?", "Color?"]

answers = []


async def get_weather(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(Form.city)
    await call.message.answer("Давайте уточним, напишите название города")


# @dp.message_handler(state=CellarImport.days)
async def days_count(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    await state.update_data(city=message.text)
    await message.answer('За какой период(в днях)?')
    await state.set_state(Form.days)
    await show_summary(message=message, data=data)


async def show_summary(message: Message, data: Dict[str, Any]) -> None:
    city = data["city"]
    days = data.get("days")
    text = f"Подведем итог. Город: {html.quote(city)}, Период: {html.quote(days)}"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())


#
#     for question in questions:
#         await asyncio.sleep(1)
#         await call.message.answer(question)
#         answers.append(call.message.text)
#
#     await call.answer()
#     await call.message.answer("Подведем итог: ")
#     result = "\n".join([f"{i + 1}. {answer}" for i, answer in enumerate(answers)])
#     await call.message.answer(result)


async def select_macbook(call: CallbackQuery, bot: Bot, callback_data: MacInfo):
    model = callback_data.model
    size = callback_data.size
    chip = callback_data.chip
    year = callback_data.year
    answer = (f'{call.message.from_user.first_name}, you choose '
              f'Apple Macbook {model} with monitor {size} inches, on chip {chip} {year} year')
    await call.message.answer(answer)
    await call.answer()