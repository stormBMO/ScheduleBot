import telebot
import requests
import sqlite3
from DB import userDataBase

#----------------------------------------------------------------------------
token_bot = '897488154:AAHM8Ghj65Xj6BP_fC8C6CWL-ZF7cs20FOA'
#----------------------------------------------------------------------------
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
               markup = generate_register_markup()
               bot.send_message(message.from_user.id, "Что ты хочешь изменить.", reply_markup=markup)
               bot.register_next_step_handler(message, edit_info)
          elif message.text == "/schedule_reg":
               register_schedule(message)
          else:
               bot.send_message(message.from_user.id, 'Не знаю что ты сказал, но я пока только понимаю команды: /whoami');

#------------------------registration`s functions-------------------------------

def register_user(message):
    bot.send_message(message.from_user.id, "Спасибо, что решил попробовать нашего бота <3")
    bot.send_sticker(message.from_user.id, 'CAADAgADJAADO2AkFPvZAoRAR-UBFgQ')
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)

def register_schedule(message):
     markup = generate_week_choose_markup()
     bot.send_message(message.from_user.id, "Отлично, приступим. Выбери неделю, которую ты хочешь заполнить - числители или знаменатель")
     bot.send_message(message.from_user.id, "Если у тебя нет разделения по неделям, то выбирай числитель", reply_markup=markup)
     #лешина часть - добавление в бд числителя знаменателя
     bot.register_next_step_handler(message, set_day)


#-------------------------------get functions-----------------------------------

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
     bot.send_message(message.from_user.id, 'Отлично! Я тебя запомнил. Ты - ' + name + ', учишься на факультете ' + faculty + 
     '\nТеперь предлагаю тебе заполнить расписание твоих занятий. Если надумаешь - пиши /schedule_reg')

#----------------------------------edit functions------------------------------

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
        bot.send_message(message.from_user.id, 'Введи новое имя.', reply_markup=keyboard_hider)
        bot.register_next_step_handler(message, edit_name)
    elif message.text == 'Факультет':
        bot.send_message(message.from_user.id, 'Введи новый факультет.', reply_markup=keyboard_hider)
        bot.register_next_step_handler(message, edit_faculty)
    else:
        bot.send_message(message.from_user.id, "ИМЯ ИЛИ ФАКУЛЬТЕТ, ДУРИК")


#----------------------------scedule functions---------------------------------

def set_day(message):
     markup = generate_day_choose_markup()
     bot.send_message(message.from_user.id, "Выбери день, который хочешь заполнить.  Если закончил добавление - пиши /stop", reply_markup=markup)
     #Леша добавляет в день который выберет
     bot.register_next_step_handler(message, set_classes)

def set_classes(message):
     user_info = userDataBase.get_user_info(message.from_user.id)
     name = user_info[0]
     if message.text == '/stop':
          bot.send_message(message.from_user.id, 'Замечательно, ' + name + '! Теперь ты можешь смотерть свое расписание в телеграмме, как крутой чел ыыыы. Рекламь его')
     else:
          day_chosen = message.text
          bot.send_message(message.from_user.id, "Теперь напиши мне пары, которые у тебя будут в " + day_chosen)
          bot.register_next_step_handler(message, set_day)

def repeat_action(message):
     bot.send_message(message.from_user.id, "Выберай следующий день. Если закончил добавление - пиши /stop")
     bot.register_next_step_handler(message, set_day)

#-----------------------------keyboards----------------------------------------

def generate_register_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton('Имя')
    button2 = telebot.types.KeyboardButton('Факультет')
    markup.row(button1, button2)
    return markup
    
def generate_day_choose_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    monday_bt = telebot.types.KeyboardButton('Понедельник')
    tuesday_bt = telebot.types.KeyboardButton('Вторник')
    wednesday_bt = telebot.types.KeyboardButton('Среда')
    thursday_bt = telebot.types.KeyboardButton('Четверг')
    friday_bt = telebot.types.KeyboardButton('Пятница')
    saturday_bt = telebot.types.KeyboardButton('Суббота')
    markup.row(monday_bt, tuesday_bt, wednesday_bt)
    markup.row(thursday_bt, friday_bt, saturday_bt)
    return markup

def generate_week_choose_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    week_1_bt = telebot.types.KeyboardButton('Числитель')
    week_2_bt = telebot.types.KeyboardButton('Знаминатель')
    markup.row(week_1_bt, week_2_bt)
    return markup


bot.polling(none_stop=True, interval=0)