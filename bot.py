import os, logging, re
import telebot
import topic_util, report
from thefuzz import process
from topic_util import char_complete_opio, char_time_status, char_default_status, char_stop_opio, char_none_report_status

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)


def edit_message(query_request, message):
    logging.info(f"Edit message-report.")
    bot.edit_message_text(chat_id=query_request.chat_id, message_id=query_request.message_id, text=message)


def set_status(query_request: topic_util.QueryRequest, opio_name: str, char_status: str):
    logging.info(f"Set stautus - {char_status} for opio -{opio_name} in report-message.")

    report_message_old = report.get_report_message(query_request.message_id, "Отчет о продажах")
    opio, probability = process.extract(opio_name, topic_util.opio_list, limit=1)[0]

    report_message_edit = re.sub(
        f'{opio} - [{char_complete_opio}{char_time_status}{char_default_status}{char_stop_opio}{char_none_report_status}]', \
        f"{opio} - {char_status}", \
        report_message_old)

    edit_message(query_request, report_message_edit)
    report.set_report_message(query_request.message_id, report_message_edit)


def send_text_with_photo(message: str, photo_file, query_request: topic_util.QueryRequest):
    logging.info(f"Send report with check photo. For tg-groupe{query_request.chat_id}.")
    bot.send_photo(query_request.chat_id, photo=photo_file, caption=message)

def send_text(message: str, query_request: topic_util.QueryRequest):
    logging.info(f"Send report. For tg-groupe{query_request.chat_id}.")
    bot.send_message(query_request.chat_id, text=message)

def send_report(report_data, photo_need, photo_file, query_request, opio_name):
    message = report.build_detailed_message(opio_name, report_data)

    if photo_need:
        send_text_with_photo(message, photo_file, query_request)
    else:
        send_text(message, query_request)

    set_status(query_request, opio_name, topic_util.char_complete_opio)

