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


def make_message_report(opio_name: str, group_topics):
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
