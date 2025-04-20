import os, logging, re
import telebot
import group, report
from thefuzz import process

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)

def set_status(query_report: group.QueryReport, opio_name: str, char_status: str):
    report_message_old = report.get("message_report")
    logging.info(f"Set stautus - {char_status} for opio -{opio_name} in report-message.")
    opio, probability = process.extract(opio_name, group.opio_list, limit=1)[0]
    report_message_edit = re.sub(
        f'{opio} - [{group.char_complete_opio}{group.char_time_status}{group.char_default_status}{group.char_stop_opio}{group.char_none_report_status}]', \
        f"{opio} - {char_status}", \
        report_message_old)
    bot.edit_message_text(chat_id=query_report.chat_id, message_id=query_report.message_id,
                                text=report_message_edit)
    logging.info(f"Edit message-report. Report from {opio} complete. Set status - {char_status}")


def send_report(report_data: str, photo_cheque, query_report: group.QueryReport, opio_name):
    logging.info(f"Create message with sales for report in tg-group. From opio-{opio_name}")
    message = report.create_message(opio_name, report_data)
    logging.info(f"Send report for sales with check photo. For tg-groupe{query_report.chat_id}.")
    bot.send_photo(query_report.chat_id, photo=photo_cheque, caption=message)
    logging.info("Set status ")
    set_status(query_report, opio_name, group.char_complete_opio)
