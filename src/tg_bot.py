import telebot
from telebot import types
from src import db_client
from src import config

# http://t.me/flat_seekerBot
BOT_NAME = 'flat_seekerBot'
bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def send_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton('Смотреть квартиры')
    markup.add(item)
    bot.send_message(message.chat.id, 'Привет, друже', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def make_post_in_tg_button(message):
    tg_posts = db_client.get_not_posted_flats()  # tuple
    if len(tg_posts) != 0:
        for tg_post in tg_posts:
            context = f'ссылка: {tg_post[0]} \n ' \
                      f'цена: {tg_post[1]} \n ' \
                      f'номер телефона: {tg_post[2]} \n ' \
                      f'город: {tg_post[3]} \n '
            bot.send_message(message.chat.id, context)
            db_client.update_not_posted_flats()
    else:
        bot.send_message(message.chat.id, 'новых квартир пока нет :(')


# make_post_in_tg_button()
# @bot.message_handler(content_types=['text'])
# def reply_button(message):
#     with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
#         with conn.cursor() as cur:
#             cur.execute('''SELECT link, price, number, city FROM flats''')
#             tg_posts = cur.fetchall()
#             for tg_post in tg_posts:  # tg_post - кортеж
#                 context = f'ссылка: {tg_post[0]} \n ' \
#                           f'цена: {tg_post[1]} \n ' \
#                           f'номер телефона: {tg_post[2]} \n ' \
#                           f'город: {tg_post[3]} \n ' \
#                           # f"фото: {tg_post[4].split(',')[0].replace('{', '')}"
#                 # bot.send_photo(message.chat.id,tg_post[4].split(',')[0].replace('{', ''))
#                 # bot.send_photo(message.chat.id, tg_post[4].split(',')[0])
#                 bot.send_message(message.chat.id, context)


bot.polling(none_stop=True, interval=1)
