import os,logging
import telebot
from telebot import types
from telebot.types import LabeledPrice, ShippingOption


BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)

def send_report(report: str):
    bot.send_message(chat_id, report)