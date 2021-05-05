#!/usr/bin/python
import threading

import telebot

API_TOKEN = '1741073741:AAFRB66ltetVTYHLVtkGWLWIZY8A1L2hyL8'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    global user_dict
    telegram_id = '@' + message.chat.username
    if telegram_id not in user_dict or user_dict[telegram_id] != message.chat.id:
        user_dict[telegram_id] = message.chat.id
        __save_bot_chats()
    bot.reply_to(message, "Hi I'm redmine notification bot!")


def send_message(telegram_id, txt):
    global user_dict
    bot.send_message(chat_id=telegram_id, text=txt)
    # if telegram_id in user_dict:
    #     if user_dict[telegram_id] is not None:
    #         bot.send_message(chat_id=user_dict[telegram_id], text=txt)


def __start_thread():
    bot.polling()


def __init_bot_chats():
    global user_dict
    file = open('telegram.cfg', 'r')
    for line in file:
        pair = line.split(':')
        telegram_id = pair[0]
        chat_id = int(pair[1])
        user_dict[telegram_id] = chat_id
    file.close()


def __save_bot_chats():
    global user_dict
    file = open('telegram.cfg', 'w')
    for telegram_id in user_dict.keys():
        chat_id = str(user_dict[telegram_id])
        file.write('{}:{}\n'.format(telegram_id, chat_id))


def start():
    __init_bot_chats()
    thread = threading.Thread(target=__start_thread)
    thread.start()
    return thread


def stop():
    __save_bot_chats()
    bot.stop_polling()