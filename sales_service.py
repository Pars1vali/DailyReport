import logging

def create_default_message(report_data: list) -> str:
    logging.info(f"Create message for count summary sales from all opio in sector.")
    message_report = f"Результаты за сектор\n"

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