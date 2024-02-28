from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from TG_API.core.utils.callbackdata import MacInfo

select_macbook = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='macbook air 13" m1 2020', callback_data='apple_air_13_m1_2020')
    ],
    [
        InlineKeyboardButton(text='macbook pro 14" m1 Pro 2021', callback_data='apple_pro_14_m1_2021')
    ],
    [
        InlineKeyboardButton(text='macbook Pro 16" 2019', callback_data='apple_pro_16_i7_2019')
    ],
    [
        InlineKeyboardButton(text='link', url='https://github.com/')
    ],
    [
        InlineKeyboardButton(text='Profile', url='tg://user?id=1961648829')
    ]
])


def get_inline_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Узнать погоду?', callback_data='weather')
    keyboard_builder.button(text='Курс валют',
                            callback_data='currency')
    # keyboard_builder.button(text='macbook pro 14" m1 Pro 2021',
    #                         callback_data=MacInfo(model='pro', size=14, chip='m1', year=2021))
    # keyboard_builder.button(text='macbook Pro 16" 2019',
    #                         callback_data=MacInfo(model='pro', size=16, chip='i7', year=2019))
    keyboard_builder.button(text='link', url='https://github.com/')
    keyboard_builder.button(text='Profile', url='tg://user?id=1961648829')
    
    keyboard_builder.adjust(1, 1, 2)
    return keyboard_builder.as_markup()