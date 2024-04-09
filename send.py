import telebot
from token import TOKEN

bot = telebot.TeleBot(TOKEN)


def get_text_messages(message):
    bot.send_message(chat_id=5255791919, text=message)

