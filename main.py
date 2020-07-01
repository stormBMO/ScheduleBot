# coding=utf-8
import telebot
import requests
import sqlite3
import transformations
from datetime import datetime
from DB import userDataBase
import transformations
# ----------------------------------------------------------------------------
token_bot = '897488154:AAHM8Ghj65Xj6BP_fC8C6CWL-ZF7cs20FOA'
# ----------------------------------------------------------------------------
bot = telebot.TeleBot(token_bot)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.from_user.username + " отправил: " + message.text)
    if not userDataBase.db_check_user(message.from_user.id):
        if message.text == "/start":
            bot.send_message(message.from_user.id, "Привет, этот бот поможет тебе с расписанием в университете. Напиши /reg, чтобы зарегистрироваться")
        elif message.text == "/help":
            bot.send_message(message.from_user.id, "Напиши /reg, чтобы зарегистрироваться")  # надо бы продумать логику тут (ответа)
        elif message.text == "/reg":
            register_user(message)
        else:
            bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    else:
        if message.text == "/whoami":
            user_info = userDataBase.get_user_info(message.from_user.id)
            name = user_info[0]
            faculty = user_info[1];
            bot.send_message(message.from_user.id, "Ты - " + name + ", учишься на факультете " + faculty);
        elif message.text == "/edit":
            markup = generate_register_markup()
            bot.send_message(message.from_user.id, "Что ты хочешь изменить.", reply_markup=markup)
            bot.register_next_step_handler(message, edit_info)
        elif message.text == "/schedule_reg":
            bot.send_message(message.from_user.id, "Отлично, приступим")
            # Добаление в бд таблицы пользователя
            userDataBase.create_schedule(message.from_user.id)
            markup = generate_day_choose_markup()
            bot.send_message(message.from_user.id, "Выбирай день недели. Если ты закончил - пиши /stop", reply_markup=markup)
            bot.register_next_step_handler(message, set_class_num)
        elif message.text == "/get_all_schedule":
            bot.send_message(message.from_user.id, "Вот твое текущее расписание:")
            bot.register_next_step_handler(message, get_all_schedule)
        else:
            bot.send_message(message.from_user.id, 'Не знаю что ты сказал, но я пока только понимаю команды: /whoami');


# ------------------------registration`s functions-------------------------------

def register_user(message):
    bot.send_message(message.from_user.id, "Спасибо, что решил попробовать нашего бота <3")
    bot.send_sticker(message.from_user.id, 'CAADAgADJAADO2AkFPvZAoRAR-UBFgQ')
    bot.send_message(message.from_user.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)


# -------------------------------get functions-----------------------------------

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
    bot.send_message(message.from_user.id, 'Теперь предлагаю тебе заполнить расписание твоих занятий. Если надумаешь - пиши /schedule_reg')


#       TODO: Add func that returns all values (classes) from users DB
def get_all_schedule(message):
    user = message.from_user.id
    userDB = userDataBase.db_get_all_schedule(user)

#       TODO: Add func that returns value from specific week day
def get_todays_schedule():
    user = 1


# ----------------------------------edit functions------------------------------

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
        bot.send_message(message.from_user.id, "Я вас не понимаю. Скажите, имя или факультет.")


# ----------------------------schedule functions---------------------------------
def set_day(message):
    markup = generate_day_choose_markup()
    bot.send_message(message.from_user.id, "Выбирай день недели. Если ты закончил - пиши /stop", reply_markup=markup)
    bot.register_next_step_handler(message, set_class_num)


def set_class_num(message):
    if message.text == '/stop':
        user_info = userDataBase.get_user_info(message.from_user.id)
        name = user_info[0]
        bot.send_message(message.from_user.id, 'Замечательно, ' + name + '! Теперь ты можешь смотерть свое расписание в телеграмe. Расскажи друзьям про бота, чтобы мы могли развиваться')
    else:
        # Здесь ставить день смотреть, какой день выбран
        userDataBase.add_weekday_flag(message.from_user.id, transformations.weekday_to_int(message.text))
        markup = generate_classes_choose_markup()
        bot.send_message(message.from_user.id, "Выбери какую пару хочешь поставить", reply_markup=markup)
        bot.register_next_step_handler(message, set_week)


def set_week(message):
    # Здесь message.text = номеру пары, на которую записывать
    userDataBase.add_number_flag(message.from_user.id, int(message.text))
    if message.text == 'Назад к выбору дня недели':
        set_day(message)
    else:
        markup = generate_week_choose_markup()
        bot.send_message(message.from_user.id, "Выбери неделю, в которую эта пара", reply_markup=markup)
        bot.register_next_step_handler(message, set_classes)


def set_classes(message):
    # Здесь message.text = либо числитель либо знаме(и)натель либо всегда
    if message.text == 'Назад к выбору пары':
        set_class_num(message)
    else:
        userDataBase.add_pair_flag(message.from_user.id, transformations.pair_to_int(message.text))
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Теперь напиши мне пары, которые у тебя будут", reply_markup=keyboard_hider)
        bot.register_next_step_handler(message, set_class_name)


def set_class_name(message):
    userDataBase.schedule_add_pair(message.from_user.id, message.text)
    bot.send_message(message.from_user.id, "Предмет добавлен.")
    set_day(message)


def repeat_action(message):
    bot.send_message(message.from_user.id, "Выбирай следующий день. Если закончил добавление - пиши /stop")
    set_day(message)


def reminder_checkpoint(message):
    bot.send_message(message.from_user.id, "")


# -----------------------------keyboards----------------------------------------

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
    week_2_bt = telebot.types.KeyboardButton('Знаменатель')
    week_all_bt = telebot.types.KeyboardButton('Всегда одинаковые пары')
    back_bt = telebot.types.KeyboardButton("Назад к выбору пары")
    markup.row(week_all_bt, week_1_bt, week_2_bt)
    markup.row(back_bt)
    return markup


def generate_classes_choose_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = (telebot.types.KeyboardButton("1"), telebot.types.KeyboardButton("2"), telebot.types.KeyboardButton("3"),
               telebot.types.KeyboardButton("4"), telebot.types.KeyboardButton("5"), telebot.types.KeyboardButton("6"),
               telebot.types.KeyboardButton("7"), telebot.types.KeyboardButton("8"))
    back_bt = telebot.types.KeyboardButton("Назад к выбору дня недели")
    markup.row(buttons[0], buttons[1], buttons[2], buttons[3])
    markup.row(buttons[4], buttons[5], buttons[6], buttons[7])
    markup.row(back_bt)
    return markup


bot.polling(none_stop=True, interval=0)
if(datetime.today().strftime('%A') == ""):
    print()