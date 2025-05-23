import logging, datetime, os, json
import redis
import util
from util import Status

r = redis.Redis(
    host=os.getenv("REDIS_IP"),
    port=os.getenv("REDIS_PORT"),
    username=os.getenv("REDIS_USER"),
    password=os.getenv("REDIS_PASSWORD")
)

def create_report_message(report_name: str, char_status):
    logging.info(f"Create report with name - {report_name}")
    date_now = datetime.datetime.now()

    report_message = f"{date_now.day:0>2}.{date_now.month:0>2} ️\n"
    report_message += f"{Status.attention} {report_name} {Status.attention}\n"
    report_message += '\n'.join([f'{opio} - {char_status}' for opio in util.get_opio_list()])

    return report_message


def get_report_message(report_id: str, report_name: str):
    logging.info(f"Get report-message for opio from tg-groupe. Get from redis storage by key - {report_id}")
    message_report_exists = r.exists(report_id)

    if message_report_exists:
        logging.info("Report-message in redis storage exists. Get message-report from redis.")
        message_report_data = r.get(report_id)
        message_report = message_report_data.decode("utf-8")
    else:
        logging.info("Report-message in redis storage doesnt exists. Create new report-message and load to redis.")
        message_report = create_report_message(report_name, util.Status.none)
        r.set(report_id, message_report)

    return message_report


def set_report_message(report_id, message_text):
    logging.info("Set new report message in redis storage.")
    r.set(report_id, message_text)


def build_detailed_message(report_data, opio_name) -> str:
    logging.info(f"Create message with sales for report in tg-group. From opio-{opio_name}")
    message_report = f"{opio_name}\n"

    for group in report_data:
        for topic in group:
            message_report += topic.get("emoji", "🟢")
            text, value = topic["text"], topic["value"]

            if topic["have_plan"] is True:
                message_report += f'\t{text} - {value["plan"]}/{value["fact"]}\n'
            elif topic["is_credit"] is True:
                message_report += f'\t{text} - {value["loan_apply"]}/{value["approved"]}/{value["issued"]}\n'
            elif topic["share"] is True:
                message_report += f'\t{text} - {value["divisible"]}/{value["divider"]}/{value["share"]}%\n'
            else:
                message_report += f'\t{text} - {value}\n'

    return message_report



def get_config(connection_query: util.ConnectionQuery):
    if connection_query.report_type == "director":
        src_path = "src/model/dopio.json"
    else:
        src_path = "src/model/sales.json"

    with open(src_path, encoding='utf-8') as file:
        model_report = json.load(file)

    return model_report