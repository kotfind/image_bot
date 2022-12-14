#!/bin/python3

from datetime import datetime
import telebot
import re
import os

from genImage import genImage
from myToken import token

bot = telebot.TeleBot(token)

usageString = '''
Send me a message with a date in format:
DD.MM.YYYY
'''

@bot.message_handler(commands=['start', 'help'])
def usage(msg):
    bot.send_message(msg.chat.id, usageString)

@bot.message_handler(content_types=['text'])
def get(msg):
    if not (res := re.search(r'^(\d{2})[.](\d{2})[.](\d{4})$', msg.text)):
        bot.send_message(msg.chat.id, 'ERROR: cannot parse')
        usage(msg)
    else:
        day, month, year = map(int, res.groups())
        date = datetime(year, month, day)

        bot.send_message(msg.chat.id, 'You image is being generated.\nPlease wait about two minutes.')

        with genImage(date.timestamp()) as file:
            file.seek(0)
            bot.send_photo(
                msg.chat.id,
                file,
                date.strftime('%d.%m.%Y')
            )

bot.infinity_polling()
