import telebot

bot = telebot.TeleBot('5501257841:AAGAIs1QeXD1HsPCrBnNqlxGyEpO1t10oi8')


def get_text_messages(message):
    bot.send_message(chat_id=5255791919, text=message)

