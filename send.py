import telebot
from Token import TOKEN, chat_id

bot = telebot.TeleBot(TOKEN)


def get_text_messages(message):
    bot.send_message(chat_id=chat_id, text=message)
