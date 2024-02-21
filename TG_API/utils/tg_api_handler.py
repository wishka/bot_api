import telebot
from telebot import types
from TG_API.utils.keyboard import kb, markup, weth_keyboard, days_key
from settings import TelegramSettings
from site_API.core import site_api, url, headers
from telebot import custom_filters
from telebot.handler_backends import State, StatesGroup #States

# States storage
from telebot.storage import StateMemoryStorage


state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TelegramSettings.TG_api_key)
method = "GET"
timeout = 15
params = {"q": "city", "days": "days"}


class MyStates(StatesGroup):
    # Just name variables differently
    city = State() # creating instances of State class is enough from now
    days = State()
    age = State()


@bot.message_handler(commands=['start'])
def start_ex(message):
    """
    Start command. Here we are starting state
    """
    bot.set_state(message.from_user.id, MyStates.city, message.chat.id)
    bot.send_message(message.chat.id, 'Hi, write me a name')


# Any state
@bot.message_handler(state="*", commands=['cancel'])
def any_state(message):
    """
    Cancel state
    """
    bot.send_message(message.chat.id, "Your state was cancelled.")
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.city)
def name_get(message):
    """
    State 1. Will process when user's state is MyStates.name.
    """
    bot.send_message(message.chat.id, 'Now write me a surname')
    bot.set_state(message.from_user.id, MyStates.days, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text


@bot.message_handler(state=MyStates.days)
def ask_age(message):
    """
    State 2. Will process when user's state is MyStates.surname.
    """
    bot.send_message(message.chat.id, "What is your age?")
    bot.set_state(message.from_user.id, MyStates.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['surname'] = message.text


# result
@bot.message_handler(state=MyStates.age, is_digit=True)
def ready_for_answer(message):
    """
    State 3. Will process when user's state is MyStates.age.
    """
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        msg = ("Ready, take a look:\n<b>"
               f"City: {data['city']}\n"
               f"Days: {data['days']}\n"
               f"Age: {message.text}</b>")
        bot.send_message(message.chat.id, msg, parse_mode="html")
    bot.delete_state(message.from_user.id, message.chat.id)


# incorrect number
@bot.message_handler(state=MyStates.age, is_digit=False)
def age_incorrect(message):
    """
    Wrong response for MyStates.age
    """
    bot.send_message(message.chat.id, 'Looks like you are submitting a string in the field age. Please enter a number')


# register filters

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())


def greetings(message):
    if message.text == 'Привет' or message.text == 'Hello':
        return _start(message)


@bot.message_handler(func=greetings)
@bot.message_handler(commands=['start'])
def _start(message):
    mes = f'Привет, <b><u>{message.from_user.first_name}</u></b>. Меня зовут Знайка!'
    bot.send_message(message.chat.id, mes, parse_mode='html')
    bot.send_message(message.chat.id, 'Вот что я умею:', reply_markup=kb)


@bot.message_handler(content_types=['website'])
def _website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Go to website', url='https://www.google.com'))
    bot.send_message(message.chat.id, "-->> to site", parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['help'])
def _get_help(message):
    bot.send_message(message.chat.id, "-->> to site", parse_mode='html', reply_markup=markup)
    

def city_select(call):
    return call.data.replace('city_', '')

def days_select(call):
    return call.data.replace('_day', '')

def querystring_formatting(call):
    params = {}
    params["q"] = city_select(call)
    params["days"] = days_select(call)
    return params


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'website':
        # Обработка команды 'website'
        pass  # Здесь должен быть код для выполнения действия
    elif call.data == 'start':
        mes = f'Привет, <b><u>{call.from_user.first_name}</u></b>. Меня зовут Знайка!'
        bot.send_message(call.message.chat.id, mes, parse_mode='html')
        bot.send_message(call.message.chat.id, 'Вот что я умею:', reply_markup=kb)
    elif call.data == 'weather':
        params = {}
        bot.send_message(call.message.chat.id, 'Я знаю, какая погода в этих городах:', reply_markup=weth_keyboard)
        params["q"] = city_select(call)
        bot.send_message(call.message.chat.id, 'За какой период?:', reply_markup=days_key)
        params["days"] = days_select(call)
        response = site_api.get_forecast_weather(method, url, headers, params=params, timeout=timeout)
        response = response.json()
        response_set = response['forecast']['forecastday'][2]['astro']
        bot.send_message(call.message.chat.id, response_set, parse_mode='html')
    elif call.data == 'coords':
        pass
    # После обработки команды - уведомление Telegram о том, что callback был обработан
    bot.answer_callback_query(call.id)


class TelegramInterface:
    @staticmethod
    def start():
        return _start
    
    @staticmethod
    def website():
        return _website
    
    @staticmethod
    def get_help():
        return _get_help
    

if __name__ == "__main__":
    _start()
    _website()
    _get_help()
    TelegramInterface()
    