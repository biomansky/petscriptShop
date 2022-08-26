import telebot
from telebot import types
from decouple import config
from Parse import parse

API_TOKEN = config('TOKEN')
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler()
def get_parse_costs(message):
    bot.send_message(message.chat.id, f'МЯУ {message.from_user.first_name} ')
    markup = types.ReplyKeyboardMarkup(row_width=5)
    price_button = types.KeyboardButton(f'Еще раз ')
    markup.add(price_button)
    bot.send_message(message.chat.id, f'Актуальные цены: {print(parse())}', reply_markup=markup)


bot.polling()
