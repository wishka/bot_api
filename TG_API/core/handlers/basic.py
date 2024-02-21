from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove
import json
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from TG_API.core.keyboards.reply import reply_keyboard, loc_tell_poll_keyboard, get_reply_keyboard
from TG_API.core.keyboards.inline import select_macbook, get_inline_keyboard


# States
class Form(StatesGroup):
    city = State()  # Will be represented in storage as 'Form:name'
    days = State()  # Will be represented in storage as 'Form:age'


storage = MemoryStorage()

questions = ["Напишите название города", "За какой период(в днях)?", "Color?"]

answers = []


async def start_get_weather(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.city)
    await message.answer(
        "Напишите название города"
    )


async def get_days(message: Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await state.set_state(Form.days)
    await message.answer("За какой период(в днях)?")
    
    
async def get_inline(message: Message, bot: Bot):
    await message.answer(f'Привет, <tg-spoiler>{message.from_user.first_name}</tg-spoiler>. Меня зовут Знайка. Вот что я умею: ->',
                         reply_markup=get_inline_keyboard())


async def get_start(message: Message, bot: Bot):
    # await bot.send_message(message.from_user.id, f"<b>Hello, {message.from_user.first_name}</b>")
    # await message.answer(f'<s>Hello, {message.from_user.first_name}</s>')
    await message.answer(f'<tg-spoiler>Hello, '
                        f'{message.from_user.first_name}</tg-spoiler>',
                        reply_markup=get_reply_keyboard())


async def get_location(message: Message, bot: Bot):
    await message.answer(
        f'You send location: \r\a<tg-spoiler>{message.location.latitude}</tg-spoiler>\r\n<tg-spoiler>{message.location.longitude}</tg-spoiler>')


async def get_photo(message: Message, bot: Bot):
    await message.answer(f'<b>Great! Its a picture</b>. I will save it')
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path, 'saved_images/photo.jpg')


async def get_hello(message: Message, bot: Bot):
    await message.answer(f'Hello and you too!')
    json_str = json.dumps(message.model_dump(), default=str)
    print(json_str)