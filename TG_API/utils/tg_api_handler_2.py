import asyncio
from aiogram import Bot, Dispatcher, types, Router
from settings import TelegramSettings
from aiogram.filters import Command
from aiogram.types import Message

bot = Bot(token=TelegramSettings.TG_api_key)
dp = Dispatcher()

questions = ["Name?", "Age?", "Color?"]

answers = []

router = Router()


@router.message(Command("start"))
async def _start(message: types.Message):
    await message.reply("Hello. I asc you some questions")
    
    for question in questions:
        await asyncio.sleep(1)
        await message.reply(question)
        response = await bot.wait_for("message")
        answers.append(response.text)
    
    await message.reply("Thank you for answers. Thats it: ")
    for i, answer in enumerate(answers, start=1):
        await message.reply(f"{i} {answer}")
        

class TelegramInterface:
    @staticmethod
    def start():
        return _start
    

if __name__ == "__main__":
    _start()
    TelegramInterface()