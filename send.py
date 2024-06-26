import telebot
from Token import TOKEN, chat_id

bot = telebot.TeleBot(TOKEN)


def get_text_messages(message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
        return True
    except Exception:
        return False
