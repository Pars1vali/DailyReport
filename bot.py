import os, logging, re
import telebot
import group
from thefuzz import process

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)


def send_report(report: str, photo_cheque, chat_id):
    bot.send_photo(chat_id, photo=photo_cheque, caption=report)


def set_report_complete(opio_name, reply_message_id, chat_id,  char_status):
    opio, probability = process.extract(opio_name, group.opio_list, limit=1)[0]
    message_text = bot.copy_message(chat_id, chat_id, reply_message_id)
    report_message = re.sub(
        f'{opio} - [{group.char_complete_opio}{group.char_time_status}{group.char_default_status}{group.char_stop_opio}{group.char_none_report_status}]',
        f"{opio} - {char_status}",
        message_text)
    bot.edit_message_text(chat_id=chat_id, message_id=reply_message_id,
                                text=report_message)
    logging.info(f"Edit message-report. Report from {opio} complete. Set status - {char_status}")
