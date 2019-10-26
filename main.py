import telebot
import requests
import sqlite3
#--------------------------------------------------------------------
token_bot = '897488154:AAHM8Ghj65Xj6BP_fC8C6CWL-ZF7cs20FOA'
name = ''
faculty = ''
#--------------------------------------------------------------------

bot = telebot.TeleBot(token_bot)

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
     print(message.from_user.username + " отправил: " + message.text) 
     if name == '':
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
     global name
     name = message.text
     bot.send_message(message.from_user.id, 'Какой у тебя факультет?')
     bot.register_next_step_handler(message, get_faculty)

def get_faculty(message):
     global faculty
     faculty = message.text
     bot.send_message(message.from_user.id, 'Отлично! Я тебя запомнил. Ты - ' + name + ', учишься на факультете ' + faculty)

def edit_name(message):
     global name
     name = message.text
     bot.send_message(message.from_user.id, 'Отлично, теперь ты ' + name + ".")

def edit_faculty(message):
     global faculty
     faculty = message.text
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
          bot.send_message(message.from_user.id, "ИМЯ ИЛИ ФАКУЛЬТЕТ, УЕБОК!")
          bot.register_next_step_handler(message, edit_info)

def generate_markup():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    button1 = telebot.types.KeyboardButton('Имя')
    button2 = telebot.types.KeyboardButton('Факультет')
    markup.row(button1, button2)
    return markup

bot.polling(none_stop=True, interval=0)