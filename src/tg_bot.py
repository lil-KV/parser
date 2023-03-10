BOT_NAME = 'flat_seekerBot'

TOKEN = ''

import telebot
from telebot import types
from src.db_client import DBNAME, USER, PASSWORD, HOST
import psycopg2

bot = telebot.TeleBot('6203659089:AAHxRiQ8dKA8fOUf5enFI4fxOMIyeqH-U2s')


@bot.message_handler(commands=['start'])
def send_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Смотреть квартиры')
    markup.add(item)
    bot.send_message(message.chat.id, 'Привет, друже', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def reply_button(message):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''SELECT link, price, number, city FROM flats''')
            tg_posts = cur.fetchall()
            for tg_post in tg_posts:  # tg_post - кортеж
                context = f'ссылка: {tg_post[0]} \n ' \
                          f'цена: {tg_post[1]} \n ' \
                          f'номер телефона: {tg_post[2]} \n ' \
                          f'город: {tg_post[3]} \n ' \
                          # f'фото: {tg_post[4].split(",")[0]}'
                # bot.send_photo(message.chat.id, tg_post[4].split(',')[0])
                # bot.send_photo(message.chat.id, tg_post[4].split(',')[0])
                bot.send_message(message.chat.id, context)



bot.polling(none_stop=True, interval=1)
