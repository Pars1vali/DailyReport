import os, logging, re
import telebot
import topic_util, report
from thefuzz import process

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)

def set_status(query_request: topic_util.QueryRequest, opio_name: str, char_status: str):
    logging.info(f"Set stautus - {char_status} for opio -{opio_name} in report-message.")

    report_message_old = report.get_report_message(query_request.message_id, "Отчет о продажах")
    opio, probability = process.extract(opio_name, topic_util.opio_list, limit=1)[0]

    report_message_edit = re.sub(
        f'{opio} - [{topic_util.char_complete_opio}{topic_util.char_time_status}{topic_util.char_default_status}{topic_util.char_stop_opio}{topic_util.char_none_report_status}]', \
        f"{opio} - {char_status}", \
        report_message_old)

    logging.info(f"Edit message-report. Report from {opio} complete. Set status - {char_status}")
    bot.edit_message_text(chat_id=query_request.chat_id, message_id=query_request.message_id,
                          text=report_message_edit)

    report.set_report_message(query_request.message_id, report_message_edit)


def send_report_with_photo(report_data: str, photo_file, query_request: topic_util.QueryRequest, opio_name):
    logging.info(f"Send report with check photo. For tg-groupe{query_request.chat_id}.")

    message = report.build_detailed_message(opio_name, report_data)
    bot.send_photo(query_request.chat_id, photo=photo_file, caption=message)
    set_status(query_request, opio_name, topic_util.char_complete_opio)


def send_report(report_data: str, query_request: topic_util.QueryRequest, opio_name):
    logging.info(f"Send report. For tg-groupe{query_request.chat_id}.")

    message = report.build_detailed_message(opio_name, report_data)
    bot.send_message(query_request.chat_id, text=message)
    set_status(query_request, opio_name, topic_util.char_complete_opio)
