import logging, json
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

    def __init__(self, is_url_correct: bool, chat_id=None, message_id=None, type_report=None):
        self.is_url_correct = is_url_correct
        self.type_report = type_report
        self.chat_id = chat_id
        self.message_id = message_id


    @staticmethod
    def create(conn_query: list):
        try:
            query_report = ConnectionQuery(is_url_correct=True)
            query_report.type_report = conn_query["type_report"]
            query_report.chat_id = conn_query["chat_id"]
            query_report.message_id = conn_query["message_id"]
        except Exception as e:
            logging.error(f"Error for get query params from url-request. Send report imposible. {e}")
            query_report.is_url_correct = False
            query_report.type_report = "sales"

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
        "Усть-Лабинск Ленина",
        "Усть-Лабинск Ободовского"
    ])


