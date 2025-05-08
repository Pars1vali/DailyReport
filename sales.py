import json
import logging
import bot, util
import sales_service
from report_service import r


def calc_credit_topic(topic: dict, index_group: int, index_topic: int, query_conn: util.ConnectionQuery) -> dict:
    topic_key = f'report:sales:{query_conn.report_id}:{index_group}:{index_topic}'
    is_topic_exists = r.exists(topic_key)

    # {
    #     "text": text_topic,
    #     "emoji": emoji,
    #     "value": {
    #         "loan_apply": loan_apply,
    #         "approved": approved,
    #         "issued": issued
    #     },
    #     "is_credit": True,
    #     "have_plan": False,
    #     "share": False
    # }

    if is_topic_exists:
        logging.info(f"Topic exists. Calculate sales-data and return result-topic. Topic-key - {topic_key}")
        topic_sum_data = r.get(topic_key)
        topic_sum = json.loads(topic_sum_data)

        topic_sum["value"] = {
            "loan_apply": topic_sum["value"]["loan_apply"] + topic["value"]["loan_apply"],
            "approved": topic_sum["value"]["approved"] + topic["value"]["approved"],
            "issued": topic_sum["value"]["issued"] + topic["value"]["issued"]
        }

        r.set(topic_key, json.dumps(topic_sum))

    else:
        logging.info("Topic doesn't exists. Set current topic as result topic and return this.")
        r.set(topic_key, json.dumps(topic))

        return topic

    return topic_sum



