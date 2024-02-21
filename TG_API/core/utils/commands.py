from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начать'
        ),
        BotCommand(
            command='help',
            description='Помощь'
        ),
        BotCommand(
            command='cancel',
            description='Отменить'
        ),
        BotCommand(
            command='inline',
            description='Показать подсказки'
        ),
        BotCommand(
            command='weather',
            description='Опции погоды'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())
