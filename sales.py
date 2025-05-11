import util, sales_service
import logging

def create_sales_message(sales_data: list):
    logging.info(f"Create sales_result message in tg-group.")
    message_report = "Отчет о продажах\n\n"

    for group in sales_data:
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

def calc(report_data: list, query_report: util.ConnectionQuery):
    sales_data = list()

    for index_group, group in enumerate(report_data):
        sales_group = list()

        for index_topic, report_topic in enumerate(group):
            if report_topic["is_credit"] is True:
                sales_topic = sales_service.calc_credit_topic(report_topic, index_group, index_topic, query_report)
            elif report_topic["have_plan"] is True:
                sales_topic = sales_service.calc_plan_topic(report_topic, index_group, index_topic, query_report)
            elif report_topic["share"] is True:
                sales_topic = sales_service.calc_share_topic(report_topic, index_group, index_topic, query_report)
            else:
                sales_topic = sales_service.calc_number_topic(report_topic, index_group, index_topic, query_report)

            sales_group.append(sales_topic)

        sales_data.append(sales_group)

    return sales_data