import bot, util
import sales_service
from report_service import r


def calculate(report_data, query_conn: util.ConnectionQuery):

    is_exists_sales_message = r.exists(f"sales:message:{query_conn.report_id}")
    if is_exists_sales_message:
        pass
    else:
        sales_message_text = sales_service.create_default_message(report_data)
        bot.send_sales_message(sales_message_text, query_conn)

