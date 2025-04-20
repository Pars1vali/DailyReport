import logging, datetime, os
import redis
import group
from group import char_attention, opio_list

r = redis.Redis(
    host=os.getenv("REDIS_IP"),
    port=os.getenv("REDIS_PORT"),
    username=os.getenv("REDIS_USER"),
    password=os.getenv("REDIS_PASSWORD")
)


def create(name: str, char_status):
    logging.info(f"Create report with name - {name}")
    date_now = datetime.datetime.now()
    report_message = f"{date_now.day:0>2}.{date_now.month:0>2} ️\n"
    report_message += f"{char_attention} {name} {char_attention}\n"
    report_message += '\n'.join([f'{opio} - {char_status}' for opio in opio_list])

    return report_message


def get(name):
    message_report_exists = r.exists(name)
    if message_report_exists:
        message_report_data = r.get(name)
        message_report = message_report_data.decode("utf-8")
    else:
        message_report = create("Отчет о продажах", group.char_none_report_status)
        r.set(name, message_report)
    return message_report


def create_message(opio_name: str, group_topics):
    message_report = f"Офис = {opio_name}\n"
    for group in group_topics:
        message_report += "🟢\n"
        for topic in group:
            if topic["have_plan"] is True:
                text, value = topic["text"], topic["value"]
                message_report += f'{text} = [{value["plan"]},{value["fact"]}]\n'
            elif topic["is_credit"] is True:
                text, value = topic["text"], topic["value"]
                message_report += f'{text} = [{value["loan_apply"]},{value["approved"]},{value["issued"]}]\n'
            else:
                message_report += f'{topic["text"]} = {topic["value"]}\n'

    return message_report
