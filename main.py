import telebot
import requests
#--------------------------------------------------------------------
token_bot = '897488154:AAHM8Ghj65Xj6BP_fC8C6CWL-ZF7cs20FOA'
#--------------------------------------------------------------------

bot = telebot.TeleBot(token_bot)

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
     print(message.text)
     if message.text == "Привет":
          bot.send_message(message.from_user.id, "Привет, хочешь добавить создать хз надо подумать") 
     elif message.text == "/help":
          bot.send_message(message.from_user.id, "Напиши привет") #надо бы продумать логику тут (ответа)
     else:
          bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)

