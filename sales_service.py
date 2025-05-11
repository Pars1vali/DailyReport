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


def calc_share_topic(topic: dict, index_group: int, index_topic: int, query_conn: util.ConnectionQuery) -> dict:
    topic_key = f'report:sales:{query_conn.report_id}:{index_group}:{index_topic}'
    is_topic_exists = r.exists(topic_key)

    # return {
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
        logging.info(f"Topic exists. Calculate sales-data and return result-topic. Topic-key - {topic_key}")
        topic_sum_data = r.get(topic_key)
        topic_sum = json.loads(topic_sum_data)

        total_divisible = topic_sum["value"]["divisible"] + topic["value"]["divisible"]
        total_divider = topic_sum["value"]["divider"] + topic["value"]["divider"]
        total_share = int(total_divider / total_divisible * 100) if total_divisible else 0

        topic_sum["value"] = {
            "divisible": total_divisible,
            "divider": total_divider,
            "share": total_share
        }

        r.set(topic_key, json.dumps(topic_sum))

    else:
        logging.info("Topic doesn't exists. Set current topic as result topic and return this.")
        r.set(topic_key, json.dumps(topic))

        return topic

    return topic_sum


def calc_plan_topic(topic: dict, index_group: int, index_topic: int, query_conn: util.ConnectionQuery) -> dict:
    topic_key = f'report:sales:{query_conn.report_id}:{index_group}:{index_topic}'
    is_topic_exists = r.exists(topic_key)

    # return {
    #     "text": topic_text,
    #     "emoji": emoji,
    #     "value": {
    #         "plan": plan,
    #         "fact": fact
    #     },
    #     "is_credit": False,
    #     "have_plan": True,
    #     "share": False
    # }

    if is_topic_exists:
        logging.info(f"Topic exists. Calculate sales-data and return result-topic. Topic-key - {topic_key}")
        topic_sum_data = r.get(topic_key)
        topic_sum = json.loads(topic_sum_data)

        topic_sum["value"] = {
            "plan": topic_sum["value"]["plan"] + topic["value"]["plan"],
            "fact": topic_sum["value"]["fact"] + topic["value"]["fact"]
        }

        r.set(topic_key, json.dumps(topic_sum))

    else:
        logging.info("Topic doesn't exists. Set current topic as result topic and return this.")
        r.set(topic_key, json.dumps(topic))

        return topic

    return topic_sum


def calc_number_topic(topic: dict, index_group: int, index_topic: int, query_conn: util.ConnectionQuery) -> dict:
    topic_key = f'report:sales:{query_conn.report_id}:{index_group}:{index_topic}'
    is_topic_exists = r.exists(topic_key)

    # return {
    #     "text": text_topic,
    #     "emoji": emoji,
    #     "value": value_topic,
    #     "is_credit": False,
    #     "have_plan": False,
    #     "share": False
    # }

    if is_topic_exists:
        logging.info(f"Topic exists. Calculate sales-data and return result-topic. Topic-key - {topic_key}")
        topic_sum_data = r.get(topic_key)
        topic_sum = json.loads(topic_sum_data)

        topic_sum["value"] += topic["value"]

        r.set(topic_key, json.dumps(topic_sum))

    else:
        logging.info("Topic doesn't exists. Set current topic as result topic and return this.")
        r.set(topic_key, json.dumps(topic))

        return topic

    return topic_sum



