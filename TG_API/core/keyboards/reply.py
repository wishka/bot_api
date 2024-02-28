from aiogram.types import KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()
    
    keyboard_builder.button(text='Send Geolocation', request_location=True)
    keyboard_builder.button(text='Send Phone', request_contact=True)
    keyboard_builder.button(text='Add Quizz', request_poll=KeyboardButtonPollType())
    keyboard_builder.adjust(2, 1)
    return keyboard_builder.as_markup(reply_keyboard=True, one_time_keyboard=True,
                                      input_field_placeholder='Send location, phone and make your own quiz')