import telebot
from telebot import types
from decouple import config
from Parse import parse
from cat_db import select_db

API_TOKEN = config('TOKEN')
bot = telebot.TeleBot(API_TOKEN)


def message_form(limit=1, price_diff=False):
    if price_diff is False:
        last_parse_info = select_db(limit)
        elem_list = []
        for elem in last_parse_info:
            elem_list.append(f''
                             f'Дата: {elem[0].strftime("%d/%m/%y")} \n'
                             f'Магазин: {elem[1]} \n'
                             f'Товар: {elem[2]} \n'
                             f'Цена: {elem[3]} \n'
                             f'-----------------------------------------\n')
        return ''.join(elem_list)
    else:
        # parse_diff_info =
        pass


@bot.message_handler(commands=['hello', 'привет', 'start'])
def hello(message):
    bot.send_message(message.chat.id, f' Доровеньки {message.from_user.first_name} ')
    bot.send_message(message.chat.id,
                     f' Пока что я умею узнавать цены на определенный кошачий корм, но это пока......\n'
                     f' Мои команды: /цены, /повтор, /разница \n'
                     f' Подробнее о командах: /помощь')


@bot.message_handler(commands=['help', 'помощь'])
def get_parse_costs(message):
    bot.send_message(message.chat.id, f'МЯУ {message.from_user.first_name} ')
    markup = types.ReplyKeyboardMarkup(row_width=5)
    price_button = types.KeyboardButton(f'Еще раз {get_repeat_costs} ')
    markup.add(price_button)
    parse()
    mess_form = message_form()
    bot.send_message(message.chat.id, f'Актуальные цены: {mess_form}', reply_markup=markup)


@bot.message_handler(commands=['repeat', 'повтор'])
def get_repeat_costs(message):
    mess_form = message_form()
    bot.send_message(message.chat.id, f'Цены сегодня:\n{mess_form}')


if __name__ == "__main__":
    bot.polling()
