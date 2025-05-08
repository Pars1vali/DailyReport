import json
import logging
import bot, util
import sales_service
from report_service import r


def calc_credit_topic(topic: dict, index_group: int, index_topic: int, query_conn: util.ConnectionQuery) -> dict:
    topic_key = f'report:sales:{query_conn.report_id}:{index_group}:{index_topic}'
    is_topic_exists = r.exists(topic_key)

    # {
    #     "text": topic_text,
    #     "emoji": emoji,
    #     "value": {
    #         "divisible": divisible,
    #         "divider": divider,
    #         "share": share_value
    #     },
    #     "is_credit": False,
    #     "have_plan": False,
    #     "share": True
    # }

    if is_topic_exists:
        logging.info("Topic exists. Calculate sales-data and return result-topic.")
        topic_sum_data = r.get(topic_key)
        topic_sum = json.loads(topic_sum_data)

        topic_sum["value"] = {
            "divisible": topic_sum["value"]["divisible"] + topic["value"]["divisible"],
            "divider": topic_sum["value"]["divider"] + topic["value"]["divider"],
            "share": topic_sum["value"]["share_value"] + topic["value"]["share_value"]
        }

        r.set(topic_key, json.dumps(topic_sum))

    else:
        logging.info("Topic doesn't exists. Set current topic as result topic and return this.")
        r.set(topic_key, json.dumps(topic))

        return topic

    return topic_sum



