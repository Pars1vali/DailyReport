import os, logging, re
import telebot
import opio, report_service
from thefuzz import process
from opio import Status

BOT_TOKEN = os.getenv("BOT_TOKEN")
chat_id = os.getenv("GROUP_CHAT_ID")

logging.getLogger().setLevel(logging.INFO)
bot = telebot.TeleBot(BOT_TOKEN)


def set_status(query_request: opio.ConnectionQuery, opio_name: str, char_status: str) -> bool:
    try:
        logging.info(f"Set stautus - {char_status} for opio -{opio_name} in report-message.")
        is_status_set = True

        report_message_old = report_service.get_report_message(query_request.message_id, "Отчет о продажах")
        opio_choose_name, probability = process.extract(opio_name, opio.get_opio_list(), limit=1)[0]

        report_message_edit = re.sub(
            f'{opio_choose_name} - [{Status.complete}{Status.time}{Status.default}{Status.stop}{Status.none}]', \
            f"{opio_choose_name} - {char_status}", \
            report_message_old)

        report_service.set_report_message(query_request.message_id, report_message_edit)
        bot.edit_message_text(chat_id=query_request.chat_id, message_id=query_request.message_id, text=report_message_edit)
        return is_status_set
    except Exception as e:
        logging.error(f"Edited message the same with new message text. {e}")
        return False


def send_report(report: report_service.ReportMessage, connection_query: opio.ConnectionQuery) -> bool:
    message = report_service.build_detailed_message(report.opio_name, report.data)
    is_status_set = set_status(connection_query, report.opio_name, Status.complete)
    is_report_send = True

    if is_status_set is False:
        logging.error(f"Status for {report.opio_name} doesn't set. Report for this opio already have.")
        return False

    if report.is_photo_need:
        logging.info(f"Send report with check photo. For tg-groupe{connection_query.chat_id}.")
        bot.send_photo(connection_query.chat_id, photo=report.photo_file, caption=message)
    else:
        logging.info(f"Send report. For tg-groupe{connection_query.chat_id}.")
        bot.send_message(connection_query.chat_id, text=message)

    return is_report_send
