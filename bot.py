import streamlit as st
import os, logging, re
import telebot
import util, report_service
from thefuzz import process
from util import Status

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)


def set_status(connection_query: util.ConnectionQuery, opio_name: str, status: str) -> bool:
    try:
        logging.info(f"Set stautus - {status} for opio -{opio_name} in report-message.")
        is_status_set = True

        report_message_old = report_service.get_report_message(connection_query.message_id, "Отчет о продажах")
        opio_choose_name, probability = process.extract(opio_name, util.get_opio_list(), limit=1)[0]

        report_message_edit = re.sub(
            f'{opio_choose_name} - [{Status.complete}{Status.time}{Status.default}{Status.stop}{Status.none}]', \
            f"{opio_choose_name} - {status}", \
            report_message_old)

        report_service.set_report_message(connection_query.message_id, report_message_edit)
        bot.edit_message_text(chat_id=connection_query.chat_id, message_id=connection_query.message_id,
                              text=report_message_edit)
        return is_status_set
    except Exception as e:
        logging.error(f"Edited message the same with new message text. {e}")
        is_status_set = False
        return is_status_set

def send_report(report: report_service.ReportMessage, connection_query: util.ConnectionQuery) -> bool:
    message = report_service.build_detailed_message(report)
    is_status_set = set_status(connection_query, report.opio_name, Status.complete)

    if is_status_set is False:
        logging.error(f"Status for {report.opio_name} doesn't set. Report for this opio already have.")
        # st.error("Отчет для этого ОПиО уже отправлен.")
        return

    if report.is_photo_need:
        logging.info(f"Send report with check photo. For tg-groupe{connection_query.chat_id}.")
        bot.send_photo(connection_query.chat_id, photo=report.photo_file, caption=message)
    else:
        logging.info(f"Send report. For tg-groupe{connection_query.chat_id}.")
        bot.send_message(connection_query.chat_id, text=message)

