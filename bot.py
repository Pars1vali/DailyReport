import os, logging, re
import telebot
import group
import redis
from thefuzz import process

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)

r = redis.Redis(
    host=os.getenv("REDIS_IP"),
    port=os.getenv("REDIS_PORT"),
    username=os.getenv("REDIS_USER"),
    password=os.getenv("REDIS_PASSWORD")
)

def send_report(report: str, photo_cheque, chat_id):
    bot.send_photo(chat_id, photo=photo_cheque, caption=report)


def get_message_report():
    message_report_data = r.get("message_report")
    message_report = message_report_data.decode("utf-8")
    return message_report



def set_status(query_report: group.QueryReport, opio_name: str, char_status: str):
    message_report = get_message_report()
    opio, probability = process.extract(opio_name, group.opio_list, limit=1)[0]
    report_message = re.sub(
        f'{opio} - [{group.char_complete_opio}{group.char_time_status}{group.char_default_status}{group.char_stop_opio}{group.char_none_report_status}]', \
        f"{opio} - {char_status}", \
        message_report)

    bot.edit_message_text(chat_id=query_report.chat_id, message_id=query_report.message_id,
                                text=report_message)
    logging.info(f"Edit message-report. Report from {opio} complete. Set status - {char_status}")
