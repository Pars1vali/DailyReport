# import streamlit as st
# import logging
# import bot, util
# import report_service
# import form_service
# from util import ConnectionQuery
#
# logging.getLogger().setLevel(logging.INFO)
#
# st.set_page_config(
#     page_title="МегаФон",
# )
#
# report_data = list()
#
#
# def create_credit_topic(topic: dict) -> dict:
#     topic_text = f'{topic["text"]} (заявки/одобрено/выдано)'
#     emoji = topic.get("emoji", "🟢")
#     help = topic.get("help", None)
#     st.markdown(f"**{topic_text}**")
#
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         loan_apply = st.number_input("Заявки", value=topic["unit"], min_value=topic["unit"], help=help,
#                                      placeholder=help,
#                                      key=f"{id(topic)}loan_apply")
#     with col2:
#         approved = st.number_input("Одобрено", value=topic["unit"], min_value=topic["unit"], help=help,
#                                    placeholder=help,
#                                    key=f"{id(topic)}approved")
#     with col3:
#         issued = st.number_input("Выдано", value=topic["unit"], min_value=topic["unit"], help=help,
#                                  placeholder=help,
#                                  key=f"{id(topic)}issued")
#
#     return {
#         "text": topic_text,
#         "emoji": emoji,
#         "value": {
#             "loan_apply": loan_apply,
#             "approved": approved,
#             "issued": issued
#         },
#         "is_credit": True,
#         "have_plan": False,
#         "share": False
#     }
#
#
# def create_plan_fact_topic(topic: dict) -> dict:
#     topic_text = f'{topic["text"]} (план/факт)'
#     emoji = topic.get("emoji", "🟢")
#     help = topic.get("help", None)
#
#     st.markdown(f"**{topic_text}**")
#
#     col1, col2 = st.columns(2)
#     with col1:
#         plan = st.number_input("План", value=topic["unit"], min_value=topic["unit"], help=help, placeholder=help,
#                                key=f"{id(topic)}plan")
#     with col2:
#         fact = st.number_input("Факт", value=topic["unit"], min_value=topic["unit"], help=help, placeholder=help,
#                                key=f"{id(topic)}fact")
#
#     return {
#         "text": topic_text,
#         "emoji": emoji,
#         "value": {
#             "plan": plan,
#             "fact": fact
#         },
#         "is_credit": False,
#         "have_plan": True,
#         "share": False
#     }
#
#
# def create_share_topic(topic: dict) -> dict:
#     topic_text = f'{topic["text"]} %'
#     emoji = topic.get("emoji", "🟢")
#     help = topic.get("help", None)
#     divisible_text = topic.get("divisible", "Число 1")
#     divider_text = topic.get("divider", "Число 2")
#
#     st.markdown(f"**{topic_text}**")
#     col1, col2 = st.columns(2)
#     with col1:
#         divisible = st.number_input(divisible_text, value=topic["unit"], min_value=topic["unit"], help=help,
#                                     placeholder=help,
#                                     key=f"{id(topic)}plan")
#     with col2:
#         divider = st.number_input(divider_text, value=topic["unit"], min_value=topic["unit"], help=help,
#                                   placeholder=help,
#                                   key=f"{id(topic)}fact")
#
#     share_value = int((divider * 100) / (divisible)) if divisible else 0
#     return {
#         "text": topic_text,
#         "emoji": emoji,
#         "value": {
#             "divisible": divisible,
#             "divider": divider,
#             "share": share_value
#         },
#         "is_credit": False,
#         "have_plan": False,
#         "share": True
#     }
#
#
# def create_number_topic(topic: dict) -> dict:
#     topic_type = topic.get("type", "number")
#     unit_name = "руб." if topic_type == "money" else "шт."
#     unit_value = topic.get("unit", 0)
#     topic_text = f'{topic["text"]}, {unit_name}'
#     emoji = topic.get("emoji", "🟢")
#     help = topic.get("help", None)
#
#     value_topic = st.number_input(topic_text,
#                                   value=unit_value,
#                                   min_value=unit_value,
#                                   help=help, placeholder=help,
#                                   key=f"{id(topic)}_number")
#
#     return {
#         "text": topic_text,
#         "emoji": emoji,
#         "value": value_topic,
#         "is_credit": False,
#         "have_plan": False,
#         "share": False
#     }
#
#
# def main():
#     connection_query = ConnectionQuery.create(st.query_params)
#     config = report_service.get_config(connection_query)
#
#     with st.form("Отчет"):
#
#         report = report_service.ReportMessage()
#         report.name = config.get("name", "Отчет")
#         report.is_photo_need = config.get("photo_need", False)
#         st.subheader(report.name)
#
#         report.opio_name = st.selectbox("Название вашего ОПиО", util.get_opio_list(), index=None, placeholder="ОПиО")
#         report.photo_file = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])
#
#         for section in config["schema"]:
#             section_data = list()
#
#             for topic in section:
#                 if topic["is_credit"] is True:
#                     topic_data = create_credit_topic(topic)
#                 elif topic["have_plan"] is True:
#                     topic_data = create_plan_fact_topic(topic)
#                 elif topic["share"] is True:
#                     topic_data = create_share_topic(topic)
#                 else:
#                     topic_data = create_number_topic(topic)
#
#                 section_data.append(topic_data)
#             report_data.append(section_data)
#
#         report.data = report_data
#         send_report_btn = st.form_submit_button("Отправить", use_container_width=True)
#
#         if send_report_btn:
#             st.write(report.data)
#             if connection_query.is_url_correct is False:
#                 st.error("Неверная ссылка. Отправить отчет не удастся.")
#             elif report.opio_name is None:
#                 st.warning("Необходимо выбрать название ОПиО")
#             elif report.is_photo_need and report.photo_file is None:
#                 st.warning("Необходимо загрузить фото отчета без гашения")
#             else:
#                 bot.send_report(report, connection_query)
#                 st.success("Отчет отправлен!")
#                 st.balloons()
#
#
# if __name__ == "__main__":
#     main()


import json
import streamlit as st
import logging
import bot, util
import report_service
from util import get_opio_list, Status

report_data = list()
logging.getLogger().setLevel(logging.INFO)

def credit_topic(topic, index_topic):
    text_topic = topic["text"]
    st.markdown(f"**{text_topic}**")

    col1, col2, col3 = st.columns(3)
    with col1:
        loan_apply = st.number_input("Заявки", value=topic["unit"], min_value=topic["unit"],
                                     key=f"{index_topic}loan_apply")
    with col2:
        approved = st.number_input("Одобрено", value=topic["unit"], min_value=topic["unit"],
                                   key=f"{index_topic}approved")
    with col3:
        issued = st.number_input("Выдано", value=topic["unit"], min_value=topic["unit"],
                                 key=f"{index_topic}issued")

    return {
        "text": text_topic,
        "value": {
            "loan_apply": loan_apply,
            "approved": approved,
            "issued": issued
        },
        "is_credit": True,
        "have_plan": False
    }

def plan_fact_topic(topic, index_group):
    text_topic = topic["text"]
    st.markdown(f"**{text_topic}**")

    col1, col2 = st.columns(2)
    with col1:
        plan = st.number_input("План", value=topic["unit"], min_value=topic["unit"], key=f"{index_group}plan")
    with col2:
        fact = st.number_input("Факт", value=topic["unit"], min_value=topic["unit"], key=f"{index_group}fact")

    return {
        "text": text_topic,
        "value": {
            "plan": plan,
            "fact": fact
        },
        "is_credit": False,
        "have_plan": True
    }

def number_topic(topic):
    value_topic = st.number_input(topic["text"], value=topic["unit"],
                                  min_value=topic["unit"])
    return {
        "text": topic["text"],
        "value": value_topic,
        "is_credit": False,
        "have_plan": False
    }

def get_query_info():
    try:
        query_report = util.ConnectionQuery(is_url_correct=True)
        query_report.report_type = st.query_params["report_type"]
        query_report.chat_id = st.query_params["chat_id"]
        query_report.message_id = st.query_params["message_id"]
    except Exception as e:
        query_report.is_url_correct = False
        query_report.report_type = "sales"
        logging.error(f"Error for get query params from url-request. Send report imposible. {e}")

    return query_report

def get_model_report(query_report: util.ConnectionQuery):
    if query_report.report_type == "director":
        src_path = "src/model/director.json"
    else:
        src_path = "src/model/sales.json"

    with open(src_path, encoding='utf-8') as file:
        model_report = json.load(file)

    return model_report

def main():
    query_report = get_query_info()
    model_report = get_model_report(query_report)

    with st.form("Отчет"):
        name_report = model_report.get("name", "Отчет")
        st.subheader(name_report)
        opio_name = st.selectbox("Название вашего ОПиО", get_opio_list(), index=None, placeholder="ОПиО")
        photo_cheque = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])

        for index_group, group in enumerate(model_report["schema"]):
            group_unit = list()
            report_data.append(group_unit)
            for index_topic, topic in enumerate(group):
                if topic["is_credit"] is True:
                    group_unit.append(credit_topic(topic, index_topic))
                elif topic["have_plan"] is True:
                    group_unit.append(plan_fact_topic(topic, index_group))
                else:
                    group_unit.append(number_topic(topic))


        send = st.form_submit_button("Отправить", use_container_width=True)

        if send:
            if query_report.url_correct is False:
                st.error("Неверная ссылка. Отправить отчет не удастся.")
            elif opio_name is None:
                st.warning("Необходимо выбрать название ОПиО")
            elif photo_cheque is None:
                st.warning("Необходимо загрузить фото отчета без гашения")
            else:
                bot.send_report(report_data, photo_cheque, query_report, opio_name)
                st.success("Отчет отправлен!")
                st.balloons()


if __name__ == "__main__":
    main()