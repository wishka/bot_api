from telebot import types


kb = types.InlineKeyboardMarkup(row_width=2)
website = types.InlineKeyboardButton(text='Website', url='https://google.com')
start = types.InlineKeyboardButton(text='Start', callback_data='start')
weather = types.InlineKeyboardButton(text='Weather', callback_data='weather')
coords = types.InlineKeyboardButton(text='Coordinates', callback_data='coordinates')
kb.add(website, start, coords, weather)

markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
start = types.KeyboardButton('Start')
help = types.KeyboardButton('Help')
markup.add(start, help,)

weth_keyboard = types.InlineKeyboardMarkup(row_width=2)
london = types.InlineKeyboardButton(text='London', callback_data='city_london')
moscow = types.InlineKeyboardButton(text='Moscow', callback_data='city_moscow')
paris = types.InlineKeyboardButton(text='Paris', callback_data='city_paris')
new_york = types.InlineKeyboardButton(text='New York', callback_data='city_new_york')
pekin = types.InlineKeyboardButton(text='Pekin', callback_data='city_pekin')
deli = types.InlineKeyboardButton(text='Deli', callback_data='city_deli')
weth_keyboard.add(london, moscow, paris, new_york, pekin, deli)

days_key = types.InlineKeyboardMarkup(row_width=2)
one = types.InlineKeyboardButton(text='1', callback_data='one_day')
three = types.InlineKeyboardButton(text='3', callback_data='three_day')
seven = types.InlineKeyboardButton(text='7', callback_data='seven_day')
days_key.add(one, three, seven)