import logging, datetime, os, re
import redis
import opio
from opio import CharStatus

r = redis.Redis(
    host=os.getenv("REDIS_IP"),
    port=os.getenv("REDIS_PORT"),
    username=os.getenv("REDIS_USER"),
    password=os.getenv("REDIS_PASSWORD")
)

# class ReportMessageService():
#
#     def __init__(self, redis_ip, redis_port, redis_user, redis_password):
#         self.redis_storage = redis.Redis(
#             host=redis_ip,
#             port=redis_port,
#             username=redis_user,
#             password=redis_password
#         )
#
#     def get(self, message_id: str, report_name: str) -> str:
#         logging.info(f"Get report-message for opio from tg-groupe. Get from redis storage by key - {message_id}")
#         message_report_exists = self.redis_storage.exists(message_id)
#         logging.info(f"Report-message in redis storage {message_report_exists}.")
#
#         if message_report_exists:
#             logging.info("Get message-report from redis.")
#             message_report_data = self.redis_storage.get(message_id)
#             message_report = message_report_data.decode("utf-8")
#         else:
#             logging.info("Create new report-message and load to redis.")
#             message_report = create_initial_report(report_name, opio.char_none_report_status)
#             self.redis_storage.set(message_id, message_report)
#
#         return message_report
#
#     def set(self, message_id, message_text):
#         logging.info("Set new report message in redis storage.")
#         self.redis_storage.set(message_id, message_text)
#
#     @staticmethod
#     def create(report_name: str, char_status: str) -> str:
#         logging.info(f"Create report with name - {report_name}")
#         date_now = datetime.datetime.now()
#
#         report_message = f"{date_now.day:0>2}.{date_now.month:0>2} ️\n"
#         report_message += f"{CharStatus.attention} {report_name} {CharStatus.attention}\n"
#         report_message += '\n'.join([f'{opio_name} - {char_status}' for opio_name in opio.get_opio_list()])
#
#         return report_message
#
#
#     @staticmethod
#     def create(opio_name: str, report_data):
#         logging.info(f"Create message with sales for report in tg-group. From opio-{opio_name}")
#
#         message_report = f"Офис: {opio_name}\n\n"
#
#         for group in report_data:
#
#             for topic in group:
#                 message_report += topic["emoji"]
#
#                 if topic["have_plan"] is True:
#                     text, value = topic["text"], topic["value"]
#                     message_report += f'\t{text} - {value["plan"]}/{value["fact"]}\n'
#                 elif topic["is_credit"] is True:
#                     text, value = topic["text"], topic["value"]
#                     message_report += f'\t{text} - {value["loan_apply"]}/{value["approved"]}/{value["issued"]}\n'
#                 elif topic["share"] is True:
#                     text, value = topic["text"], topic["value"]
#                     message_report += f'\t{text} - {value["divisible"]}/{value["divider"]}/{value["share"]}%\n'
#                 else:
#                     message_report += f'\t{topic["text"]} - {topic["value"]}\n'
#
#         return message_report



def create_initial_report(name: str, char_status):
    logging.info(f"Create report with name - {name}")
    date_now = datetime.datetime.now()

    report_message = f"{date_now.day:0>2}.{date_now.month:0>2} ️\n"
    report_message += f"{CharStatus.attention} {name} {CharStatus.attention}\n"
    report_message += '\n'.join([f'{opio} - {char_status}' for opio in opio.get_opio_list()])

    return report_message


def get_report_message(message_id: str, name_report: str):
    logging.info(f"Get report-message for opio from tg-groupe. Get from redis storage by key - {message_id}")
    message_report_exists = r.exists(message_id)
    logging.info(f"Report-message in redis storage {message_report_exists}.")

    if message_report_exists:
        logging.info("Get message-report from redis.")
        message_report_data = r.get(message_id)
        message_report = message_report_data.decode("utf-8")
    else:
        logging.info("Create new report-message and load to redis.")
        message_report = create_initial_report(name_report, opio.char_none_report_status)
        r.set(message_id, message_report)

    return message_report


def set_report_message(message_id, message_text):
    logging.info("Set new report message in redis storage.")
    r.set(message_id, message_text)


def build_detailed_message(opio_name: str, report_data):
    logging.info(f"Create message with sales for report in tg-group. From opio-{opio_name}")

    message_report = f"Офис: {opio_name}\n\n"

    for group in report_data:

        for topic in group:
            message_report += topic["emoji"]

            if topic["have_plan"] is True:
                text, value = topic["text"], topic["value"]
                message_report += f'\t{text} - {value["plan"]}/{value["fact"]}\n'
            elif topic["is_credit"] is True:
                text, value = topic["text"], topic["value"]
                message_report += f'\t{text} - {value["loan_apply"]}/{value["approved"]}/{value["issued"]}\n'
            elif topic["share"] is True:
                text, value = topic["text"], topic["value"]
                message_report += f'\t{text} - {value["divisible"]}/{value["divider"]}/{value["share"]}%\n'
            else:
                message_report += f'\t{topic["text"]} - {topic["value"]}\n'

    return message_report

