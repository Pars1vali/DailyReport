char_default_status = "➖"
char_complete_opio = "✅"
char_stop_opio = "⛔"
char_attention = "❗"
char_time_status = "⌛"
char_none_report_status = "❌"

opio_list = list([
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


class QueryReport:
    def __init__(self, url_correct: bool, chat_id=None, chat_type=None, message_id=None, message_date=None, type_report=None):
        self.url_correct = url_correct
        self.type_report = type_report
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.message_id = message_id
        self.message_date = message_date



def make_message_report(opio_name: str, group_topics):
    message_report = "/cross\n"
    message_report += f"Офис = {opio_name}\n"
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
