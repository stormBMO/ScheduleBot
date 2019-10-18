import telebot
import requests
#--------------------------------------------------------------------
token_bot = '897488154:AAHM8Ghj65Xj6BP_fC8C6CWL-ZF7cs20FOA'
name = ''

#--------------------------------------------------------------------

bot = telebot.TeleBot(token_bot)

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
     print(message.from_user.username + " отправил: " + message.text)
     if message.text == "/help":
          bot.send_message(message.from_user.id, "Напиши /reg, чтобы зарегистрироваться") #надо бы продумать логику тут (ответа)
     elif message.text == "/reg" :
          bot.send_message(message.from_user.id, "Завтра допишу что-нибудь, а пока что вот:")
          bot.send_sticker(message.from_user.id, 'CAADAgADJAADO2AkFPvZAoRAR-UBFgQ')
     else:
          bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)