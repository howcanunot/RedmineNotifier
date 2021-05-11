#!/usr/bin/python
import threading
from logger import logger
from redmine_issue_monitor import get_issues_assigned_to, update_issue
import SQLHelper

import telebot
from telebot import types

API_TOKEN = '1741073741:AAEDqUc_0nwAub2skv44LjOzM3udm6C4mMw'


bot = telebot.TeleBot(API_TOKEN)

user_dict = {}
flag = False


def __init_markup():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(types.KeyboardButton(text='Update Issue'))
    return keyboard


def __init_inline_markup(telegram_id):
    sql_helper = SQLHelper.SQLHelper('database.sqlite')
    redmine_user_id = sql_helper.get_user(telegram_id)[1]
    user_issues = sorted(get_issues_assigned_to(redmine_user_id), key=lambda x: x.id)

    markup = types.InlineKeyboardMarkup(row_width=3)
    for issue in user_issues:
        markup.add(types.InlineKeyboardButton('Issue #{}: {}'.format(issue.id, issue.subject), callback_data=issue.id))

    return markup


@bot.callback_query_handler(func=lambda call: True)
def event_handler(call):

    updates = {'new': 1, 'in progress': 2, 'resolved': 3, 'feedback': 4, 'closed': 5}

    if call.data.isnumeric():
        issue_id = call.data.split(':')[0][call.data.split(':')[0].find('#') + 1:]
        markup = types.InlineKeyboardMarkup()
        buttons = []
        for key in updates:
            buttons.append(types.InlineKeyboardButton(key.capitalize(), callback_data='{}-{}'.format(issue_id, key)))
        markup.add(*buttons)
        bot.send_message(call.message.chat.id, text='<b>Select status for issue #{}:</b>'.format(issue_id),
                         parse_mode='HTML', reply_markup=markup)
    else:
        try:
            data = call.data.split('-')
            issue_id, new_status = data[0], data[1]
            update_issue(issue_id, updates[new_status])
            bot.send_message(call.message.chat.id, text='Issue updated!')
        except Exception as exception:
            bot.send_message(call.message.chat.id, text='Raised exception: {}'.format(exception))
            return


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    global user_dict
    telegram_id = '@' + message.chat.username
    if telegram_id not in user_dict:
        bot.reply_to(message, "It looks like you are not registered in the system. Connect with @vchernokulsky"
                                      " for help")
        return
    if user_dict[telegram_id] != message.chat.id:
        user_dict[telegram_id] = message.chat.id
        __save_bot_chats()
    bot.reply_to(message, "Hi I'm redmine notification bot!", reply_markup=__init_markup())


@bot.message_handler(content_types=['text'])
def get_new_status(message):
    try:
        if message.chat.username in user_dict and message.text == 'Update Issue':
            bot.send_message(message.chat.id, text='Issues assigned to you:',
                             reply_markup=__init_inline_markup(message.chat.id))
    except Exception as exception:
        bot.send_message(message.chat.id, text='Raised exception: {}'.format(exception))
        return


def send_message(telegram_id, txt):
    global user_dict
    bot.send_message(chat_id=telegram_id, text=txt)


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
    try:
        __init_bot_chats()
        thread = threading.Thread(target=__start_thread)
        thread.start()
        return thread
    except Exception as exception:
        logger.critical('Raised exception while running bot: {}'.format(exception))


def stop():
    __save_bot_chats()
    bot.stop_polling()