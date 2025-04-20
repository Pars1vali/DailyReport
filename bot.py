import os, logging, re
import telebot
import group, report
from thefuzz import process

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)

def send_report(message: str, photo_cheque, query_report: group.QueryReport):
    bot.send_photo(query_report.chat_id, photo=photo_cheque, caption=message)


def set_status(query_report: group.QueryReport, opio_name: str, char_status: str):
    message_report = report.get("message_report")
    opio, probability = process.extract(opio_name, group.opio_list, limit=1)[0]
    report_message = re.sub(
        f'{opio} - [{group.char_complete_opio}{group.char_time_status}{group.char_default_status}{group.char_stop_opio}{group.char_none_report_status}]', \
        f"{opio} - {char_status}", \
        message_report)

    bot.edit_message_text(chat_id=query_report.chat_id, message_id=query_report.message_id,
                                text=report_message)
    logging.info(f"Edit message-report. Report from {opio} complete. Set status - {char_status}")
