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
     if message.text == "/help":
          bot.send_message(message.from_user.id, "Этот бот поможет тебе с расписанием в университете. Напиши /reg, чтобы зарегистрироваться") #надо бы продумать логику тут (ответа)
     elif message.text == "/reg" :
          bot.send_message(message.from_user.id, "Завтра допишу что-нибудь, а пока что вот:")
          bot.send_sticker(message.from_user.id, 'CAADAgADJAADO2AkFPvZAoRAR-UBFgQ')
          bot.register_next_step_handler(message, get_name)
     else:
          bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def get_name (message):
     name = message.text
     bot.send_message(message.from_user.id, 'Какой у тебя факультет?')
     bot.register_next_step_handler(message, get_faculty)


def get_faculty(message):
     faculty = message.text
     bot.send_message(message.from_user.id, 'Отлично! Я тебя запомнил. Ты - ' + name + ', учишься на факультете ' + faculty)

bot.polling(none_stop=True, interval=0)