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



class QueryRequest:

    def __init__(self, is_url_correct: bool, chat_id=None, message_id=None, type_report=None):
        self.is_url_correct = is_url_correct
        self.type_report = type_report
        self.chat_id = chat_id
        self.message_id = message_id


    @staticmethod
    def create(query_params: list):
        try:
            query_report = QueryRequest(is_url_correct=True)
            query_report.type_report = query_params["type_report"]
            query_report.chat_id = query_params["chat_id"]
            query_report.message_id = query_params["message_id"]
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


def get_report_config(query_request: QueryRequest):
    if query_request.type_report == "director":
        src_path = "src/model/director.json"
    else:
        src_path = "src/model/sales.json"

    with open(src_path, encoding='utf-8') as file:
        model_report = json.load(file)

    return model_report