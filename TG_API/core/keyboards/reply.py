from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Row 1. ClickButton 1'
        ),
        KeyboardButton(
            text='Row 1. ClickButton 2'
        ),
        KeyboardButton(
            text='Row 1. ClickButton 3'
        ),
    ],
    [
        KeyboardButton(
            text='Row 2. ClickButton 1'
        ),
        KeyboardButton(
            text='Row 2. ClickButton 2'
        ),
        KeyboardButton(
            text='Row 2. ClickButton 3'
        ),
        KeyboardButton(
            text='Row 2. ClickButton 4'
        ),
    ],
    [
        KeyboardButton(
            text='Row 3. ClickButton 1'
        ),
        KeyboardButton(
            text='Row 3. ClickButton 2'
        ),
    ]
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Choose button')

loc_tell_poll_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(
            text='Send Geolocation',
            request_location=True
        )
    ],
    [
        KeyboardButton(
            text='Send self contact',
            request_contact=True
        )
    ],
    [
        KeyboardButton(
            text='Create Polling',
            request_poll=KeyboardButtonPollType()
            # quiz - викторина, regular - опрос с несколькими вариантами ответов
        )
    ],
], resize_keyboard=True, one_time_keyboard=False,
    input_field_placeholder='Send location, phone and make your own quiz')


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    
    keyboard_builder.button(text='Button 1')
    keyboard_builder.button(text='Button 2')
    keyboard_builder.button(text='Button 3')
    keyboard_builder.button(text='Send Geolocation', request_location=True)
    keyboard_builder.button(text='Send Phone', request_contact=True)
    keyboard_builder.button(text='Add Quizz', request_poll=KeyboardButtonPollType())
    keyboard_builder.adjust(3, 2, 1)
    return keyboard_builder.as_markup(reply_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Send location, phone and make your own quiz')