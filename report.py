import os
import logging
import datetime
import redis
from typing import List
import topic_util


class ReportService:
    def __init__(self):
        redis_host = os.getenv("REDIS_IP")
        redis_port = int(os.getenv("REDIS_PORT", 6379))
        redis_user = os.getenv("REDIS_USER")
        redis_password = os.getenv("REDIS_PASSWORD")

        if not redis_host:
            raise ValueError("REDIS_IP не задан")

        self.redis = redis.Redis(
            host=redis_host,
            port=redis_port,
            username=redis_user,
            password=redis_password
        )

    def get_report_message(self, name: str) -> str:
        logging.info(f"Получение отчета из Redis по ключу: {name}")
        if self.redis.exists(name):
            message = self.redis.get(name).decode("utf-8")
            logging.info("Сообщение найдено в Redis")
        else:
            logging.info("Создание нового сообщения и сохранение в Redis")
            message = self.build_initial_report(name, topic_util.char_none_report_status)
            self.redis.set(name, message)
        return message

    def set_report_message(self, name: str, data: str) -> None:
        logging.info(f"Сохранение отчета в Redis по ключу: {name}")
        self.redis.set(name, data)

    def build_initial_report(self, name: str, char_status: str) -> str:
        logging.info(f"Создание начального отчета с именем: {name}")
        date_now = datetime.datetime.now()
        report_message = f"{date_now.day:02}.{date_now.month:02} ️\n"
        report_message += f"{topic_util.char_attention} {name} {topic_util.char_attention}\n"
        report_message += '\n'.join([f'{opio} - {char_status}' for opio in topic_util.opio_list])
        return report_message

    def build_detailed_report(self, opio_name: str, group_topics: List[List[dict]]) -> str:
        logging.info("Формирование детализированного сообщения")
        message_report = f"Офис = {opio_name}\n"
        for group in group_topics:
            for topic in group:
                message_report += topic["emoji"]
                text = topic["text"]
                value = topic["value"]

                if topic.get("have_plan"):
                    message_report += f'\t{text} - {value["plan"]}/{value["fact"]}\n'
                elif topic.get("is_credit"):
                    message_report += f'\t{text} - {value["loan_apply"]}/{value["approved"]}/{value["issued"]}\n'
                elif topic.get("share"):
                    message_report += f'\t{text} - {value["value_1"]}/{value["value_2"]}/{value["share"]}%\n'
                else:
                    message_report += f'\t{text} - {value}\n'

        return message_report
