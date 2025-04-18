import os, logging, re
import telebot
from watchdog.observers.fsevents2 import message
import group
from thefuzz import process

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)


def send_report(report: str, photo_cheque, chat_id):
    bot.send_photo(chat_id, photo=photo_cheque, caption=report)


def set_status(query_report: group.QueryReport):
    message_chat = telebot.types.Chat(query_report.chat_id, query_report.chat_type)
    message = telebot.types.Message(message_id=query_report.message_id,
                                    chat=message_chat,
                                    content_type=["text"],
                                    date=query_report.message_date,
                                    options={},
                                    json_string="")

    print(message)


