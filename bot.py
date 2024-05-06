import logging
import telebot
from config import config
from database import create_database

bot = telebot.TeleBot(token=config['CREDENTIALS']['BOT_TOKEN'])


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, 'Кушман')
    create_database()

bot.polling()