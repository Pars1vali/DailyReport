import json
import streamlit as st
import logging
import bot, topic_util
from topic_util import opio_list
from topic import share, credit, plan_fact, number

logging.getLogger().setLevel(logging.INFO)

def get_query_info():
    try:
        query_request = topic_util.QueryRequest(is_url_correct=True)
        query_request.type_report = st.query_params["type_report"]
        query_request.chat_id = st.query_params["chat_id"]
        query_request.message_id = st.query_params["message_id"]
    except Exception as e:
        logging.error(f"Error parsing URL query params: {e}")
        return topic_util.QueryRequest(is_url_correct=False, type_report="sales")

    return query_request

def get_model_report(query_request: topic_util.QueryRequest):
    if query_request.type_report == "director":
        src_path = "src/model/director.json"
    else:
        src_path = "src/model/sales.json"

    with open(src_path, encoding='utf-8') as file:
        model_report = json.load(file)

    return model_report

# def get_photo(photo_need: bool):
#     photo = None
#     if photo_need:
#         photo = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])
#
#     return photo

def send_report(opio_name: str, photo_need: bool, photo_file, query_request, report_data):
    if not query_request.is_url_correct:
        st.error("Неверная ссылка. Отправить отчет не удастся.")
        return

    if not opio_name:
        st.warning("Необходимо выбрать название ОПиО.")
        return

    if photo_need and photo_file is None:
        st.warning("Необходимо загрузить фото отчета без гашения.")
        return

    try:
        if photo_need:
            bot.send_report_with_photo(report_data, photo_file, query_request, opio_name)
        else:
            bot.send_report(report_data, query_request, opio_name)

        st.success("Отчет отправлен!")
        st.balloons()
        
    except Exception as e:
        logging.exception("Ошибка при отправке отчета:")
        st.error(f"Произошла ошибка при отправке отчета: {e}")

def build_report_groups(model_report):
    report_data = []
    for index_group, group in enumerate(model_report["topics"]):
        group_unit = []
        for index_topic, topic in enumerate(group):
            if topic.get_report_message("is_credit"):
                group_unit.append(credit(topic, index_topic))
            elif topic.get_report_message("have_plan"):
                group_unit.append(plan_fact(topic, index_group))
            elif topic.get_report_message("share"):
                group_unit.append(share(topic, index_topic))
            else:
                group_unit.append(number(topic, index_group, index_topic))
        report_data.append(group_unit)
    return report_data


def main():
    query_request = get_query_info()
    model_report = get_model_report(query_request)

    with st.form("Отчет"):
        name_report = model_report.get("name", "Отчет")
        photo_need = model_report.get("photo_need", False)

        st.subheader(name_report)
        opio_name = st.selectbox("Название вашего ОПиО", opio_list, index=None, placeholder="ОПиО")
        photo_file = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"], disabled=True)

        report_data = build_report_groups(model_report)

        st.form_submit_button(
            "Отправить",
            use_container_width=True,
            on_click=send_report,
            args=[opio_name, photo_need, photo_file, query_request, report_data]
        )


if __name__ == "__main__":
    main()