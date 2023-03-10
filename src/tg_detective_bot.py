import telebot
from src import config

# http://t.me/parser_detectiveBot
bot = telebot.TeleBot(config.DETECTIVE_BOT_TOKEN)


def send_tg_post(message):
    bot.send_message(config.REPORT_GROUP_ID, message, parse_mode='html')
