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


class QueryRequest:
    def __init__(self, is_url_correct: bool, chat_id=None, chat_type=None, message_id=None, message_date=None, type_report=None):
        self.is_url_correct = is_url_correct
        self.type_report = type_report
        self.chat_id = chat_id
        self.chat_type = chat_type
        self.message_id = message_id
        self.message_date = message_date
