import telebot
from decouple import config

API_TOKEN = config('TOKEN', )
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def mew_message(message):
    bot.send_message(message.chat.id, f'МЯУ {message.from_user.first_name} ')


bot.polling()
