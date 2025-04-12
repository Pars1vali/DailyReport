import os, logging
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)


def send_report(report: str, photo_cheque):
    bot.send_photo(chat_id, photo=photo_cheque, caption=report)
