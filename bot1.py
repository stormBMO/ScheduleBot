import telebot;
bot = telebot.TeleBot('%897488154:AAHM8Ghj65Xj6BP_fC8C6CWL-ZF7cs20FOA%');

@bot.message_handler(content_types=['text'])

def get_text_messages(message):
     if message.text == "Привет":
          bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
     elif message.text == "/help":
          bot.send_message(message.from_user.id, "Напиши привет")
     else:
          bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

bot.polling(none_stop=True, interval=0)