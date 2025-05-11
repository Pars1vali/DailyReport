import logging
from dataclasses import dataclass


@dataclass
class Status:
    default: str = "➖"
    complete: str = "✅"
    stop: str = "⛔"
    attention: str = "❗"
    time: str = "⌛"
    none: str = "❌"


class ConnectionQuery:

    def __init__(self, is_url_correct: bool, chat_id=None, report_id=None, sales_id=None, report_type=None):
        self.is_url_correct = is_url_correct
        self.report_type = report_type
        self.chat_id = chat_id
        self.report_id = report_id
        self.sales_id = sales_id

    @staticmethod
    def create(conn_query: list):
        try:
            query_report = ConnectionQuery(is_url_correct=True)
            query_report.report_type = conn_query["report_type"]
            query_report.chat_id = conn_query["chat_id"]
            query_report.report_id = conn_query["report_id"]
            query_report.sales_id = conn_query["sales_id"]
        except Exception as e:
            logging.error(f"Error for get query params from url-request. Send report imposible. {e}")
            query_report.is_url_correct = False
            query_report.report_type = "sales"

        return query_report


def get_opio_list():
    return list([
        "Став 189",
        "Став 141",
        "Став/Веш",
        "Лента",
        "Оз",
        "Мачуги",
        "Игнатова",
        "Сормовская",
        "Тюляева",
        "Новомих",
        "Гулькевичи",
        "Туапсе Маркса",
        "Туапсе Жукова",
        "Кропоткин 226",
        "Кропоткин 72",
        "Ленина",
        "Ободовского"
    ])
