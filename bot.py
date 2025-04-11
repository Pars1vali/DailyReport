import os,logging
from aiogram import Bot

logging.getLogger().setLevel(logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)

chat_id = "7405295017"

def send_report(report: str):
    bot.send_message(chat_id, report)