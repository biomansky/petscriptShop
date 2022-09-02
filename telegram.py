import telebot
from decouple import config
from Parse import parse
from cat_db import select_db, price_diff_db

API_TOKEN = config('TOKEN')
bot = telebot.TeleBot(API_TOKEN)


def message_form(limit=1, price_diff=False):
    elem_list = []
    if price_diff is False:
        last_parse_info = select_db(limit)
        for elem in last_parse_info:
            elem_list.append(f''
                             f'Дата: {elem[0].strftime("%d/%m/%y")} \n'
                             f'Магазин: {elem[1]} \n'
                             f'Товар: {elem[2]} \n'
                             f'Цена: {elem[3]} \n'
                             f'-----------------------------------------\n')
        return ''.join(elem_list)
    else:
        diff_parse_info = price_diff_db()
        for elem in diff_parse_info:
            dict_date = dict(zip([date.strftime("%d/%m/%y") for date in elem[1][2::2]],
                                 [value for value in elem[1][1::2]]))
            str_from_dict = ''
            for key, value in dict_date.items():
                str_from_dict += f'|{key} - {value}|'
            elem_list.append(f''
                             f'{elem[0]}\n'
                             f'{elem[1][0]}: '
                             f'{str_from_dict}\n'
                             f'-----------------------------------------\n')
        return ''.join(elem_list)


@bot.message_handler(commands=['hello', 'привет', 'start', 'старт'])
def hello(message):
    bot.send_message(message.chat.id, f' Доровеньки {message.from_user.first_name} ')
    bot.send_message(message.chat.id,
                     f' Пока что я умею узнавать цены на определенный кошачий корм, но это пока......\n'
                     f' Мои команды: /цены, /повтор, /разница \n'
                     f' Подробнее о командах: /помощь')


@bot.message_handler(commands=['price', 'цены', 'цена'])
def get_parse_costs(message):
    bot.send_message(message.chat.id, f'МЯУ {message.from_user.first_name} ')
    parse()
    mess_form = message_form()
    bot.send_message(message.chat.id, f'Актуальные цены: {mess_form}')


@bot.message_handler(commands=['help', 'помощь'])
def get_parse_costs(message):
    bot.send_message(message.chat.id, 'Команда /цены проверяет последние актуальные цены в магазине \n'
                                      'Команда /повтор показывает последнюю цену из БД \n'
                                      'Команда /разница показывает динамику изменения цен на товары')


@bot.message_handler(commands=['repeat', 'повтор'])
def get_repeat_costs(message):
    mess_form = message_form()
    bot.send_message(message.chat.id, f'Цены сегодня:\n'
                                      f'{mess_form}')


@bot.message_handler(commands=['difference', 'разница'])
def get_repeat_costs(message):
    mess_form = message_form(price_diff=True)
    bot.send_message(message.chat.id, f'Как менялись цены на:\n'
                                      f'{mess_form}')


if __name__ == "__main__":
    bot.polling()
