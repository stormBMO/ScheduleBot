import telebot
import requests
import sqlite3
from DB import userDataBase

#--------------------------------------------------------------------
token_bot = '897488154:AAHM8Ghj65Xj6BP_fC8C6CWL-ZF7cs20FOA'
#--------------------------------------------------------------------
bot = telebot.TeleBot(token_bot)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
     print(message.from_user.username + " отправил: " + message.text)
     if not userDataBase.db_check_user(message.from_user.id):
          if message.text == "/start":
               bot.send_message(message.from_user.id, "Привет, этот бот поможет тебе с расписанием в университете. Напиши /reg, чтобы зарегистрироваться")
          elif message.text == "/help":
               bot.send_message(message.from_user.id, "Напиши /reg, чтобы зарегистрироваться") #надо бы продумать логику тут (ответа)
          elif message.text == "/reg":
               register_user(message)
          else:
               bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
     else:
          if message.text == "/whoami":
               user_info = userDataBase.get_user_info(message.from_user.id)
               name = user_info[0]
               faculty = user_info[1];
               bot.send_message(message.from_user.id, "Ты - " + name + ", учишься на факультете "  + faculty);
          elif message.text == "/edit":
               markup = generate_markup()
               bot.send_message(message.from_user.id, "Что ты хочешь изменить.", reply_markup=markup)
               bot.register_next_step_handler(message, edit_info)
          else:
               bot.send_message(message.from_user.id, 'Не знаю что ты сказал, но я пока только понимаю команды: /whoami');


def register_user(message):
     bot.send_message(message.from_user.id, "Спасибо, что решил попробовать нашего бота <3")
     bot.send_sticker(message.from_user.id, 'CAADAgADJAADO2AkFPvZAoRAR-UBFgQ')
     bot.send_message(message.from_user.id, "Как тебя зовут?")
     bot.register_next_step_handler(message, get_name)


def get_name(message):
     name = message.text
     userDataBase.add_user_to_db(message.from_user.id, name)
     bot.send_message(message.from_user.id, 'Какой у тебя факультет?')
     bot.register_next_step_handler(message, get_faculty)


def get_faculty(message):
     faculty = message.text
     userDataBase.db_update_faculty(message.from_user.id, faculty)
     user_info = userDataBase.get_user_info(message.from_user.id)
     name = user_info[0]
     faculty = user_info[1]
     bot.send_message(message.from_user.id, 'Отлично! Я тебя запомнил. Ты - ' + name + ', учишься на факультете ' + faculty)


def edit_name(message):
     name = message.text
     userDataBase.db_update_name(message.from_user.id, name)
     bot.send_message(message.from_user.id, 'Отлично, теперь ты ' + name + ".")


def edit_faculty(message):
     faculty = message.text
     userDataBase.db_update_faculty(message.from_user.id, faculty)
     bot.send_message(message.from_user.id, 'Супер, теперь ты учишься на факультет ' + faculty + ".")


def edit_info(message):
     keyboard_hider = telebot.types.ReplyKeyboardRemove()
     if message.text == 'Имя':
          bot.send_message(message.from_user.id, 'Введи новое имя.',reply_markup=keyboard_hider)
          bot.register_next_step_handler(message, edit_name)
     elif message.text == 'Факультет':
          bot.send_message(message.from_user.id, 'Введи новый факультет.', reply_markup=keyboard_hider)
          bot.register_next_step_handler(message, edit_faculty)
     else:
          bot.send_message(message.from_user.id, "ИМЯ ИЛИ ФАКУЛЬТЕТ, ДУРИК")


def generate_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Имя')
    button2 = telebot.types.KeyboardButton('Факультет')
    markup.row(button1, button2)
    return markup


bot.polling(none_stop=True, interval=0)