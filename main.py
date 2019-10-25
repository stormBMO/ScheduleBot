import telebot
import requests
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
          if message.text == "/help":
               bot.send_message(message.from_user.id, "Этот бот поможет тебе с расписанием в университете. Напиши /reg, чтобы зарегистрироваться") #надо бы продумать логику тут (ответа)
          elif message.text == "/reg":
               bot.send_message(message.from_user.id, "Спасибо, что решил попробовать нашего бота <3")
               bot.send_sticker(message.from_user.id, 'CAADAgADJAADO2AkFPvZAoRAR-UBFgQ')
               bot.send_message(message.from_user.id, "Как тебя зовут?")
               bot.register_next_step_handler(message, get_name)
          else:
               bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
     else:
               if message.text == "/whoami":
                    bot.send_message(message.from_user.id, 'Ты - ' + name + ', учишься на факультете ' + faculty);
               else:
                    bot.send_message(message.from_user.id, 'Не знаю что ты сказал, но я пока только понимаю команды: /whoami');



def get_name(message):
     global name 
     name = message.text
     bot.send_message(message.from_user.id, 'Какой у тебя факультет?')
     bot.register_next_step_handler(message, get_faculty)


def get_faculty(message):
     global faculty
     faculty = message.text
     bot.send_message(message.from_user.id, 'Отлично! Я тебя запомнил. Ты - ' + name + ', учишься на факультете ' + faculty)

bot.polling(none_stop=True, interval=0)