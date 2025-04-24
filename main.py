import json
import streamlit as st
import logging
import bot, topic_util, topic, report
from topic_util import opio_list, char_complete_opio
from topic import share, credit, plan_fact, number

logging.getLogger().setLevel(logging.INFO)

def get_query_info():
    try:
        query_report = topic_util.QueryRequest(is_url_correct=True)
        query_report.type_report = st.query_params["type_report"]
        query_report.chat_id = st.query_params["chat_id"]
        query_report.message_id = st.query_params["message_id"]
    except Exception as e:
        query_report.is_url_correct = False
        query_report.type_report = "sales"
        logging.error(f"Error for get query params from url-request. Send report imposible. {e}")

    return query_report

def get_model_report(query_report: topic_util.QueryRequest):
    if query_report.type_report == "director":
        src_path = "src/model/director.json"
    else:
        src_path = "src/model/sales.json"

    with open(src_path, encoding='utf-8') as file:
        model_report = json.load(file)

    return model_report

def build_report_form(model_report):
    report_data = list()

    for index_group, group in enumerate(model_report["topics"]):
        group_unit = list()
        report_data.append(group_unit)
        for index_topic, topic in enumerate(group):
            if topic["is_credit"] is True:
                group_unit.append(credit(topic, index_topic))
            elif topic["have_plan"] is True:
                group_unit.append(plan_fact(topic, index_group))
            elif topic["share"] is True:
                group_unit.append(share(topic, index_topic))
            else:
                group_unit.append(number(topic, index_group, index_topic))

    return report_data

def send_report(report_data, photo_need, photo_file, query_request, opio_name):
    if photo_need:
        bot.send_report_with_photo(report_data, photo_file, query_request, opio_name)
    else:
        bot.send_report(report_data, query_request, opio_name)

    st.success("Отчет отправлен!")
    st.balloons()

def main():
    query_request = get_query_info()
    model_report = get_model_report(query_request)

    with st.form("Отчет"):
        name_report = model_report.get("name", "Отчет")
        photo_need = model_report.get("photo_need", False)

        st.subheader(name_report)
        opio_name = st.selectbox("Название вашего ОПиО", opio_list, index=None, placeholder="ОПиО")
        photo_file = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])

        report_data = build_report_form(model_report)

        send = st.form_submit_button("Отправить", use_container_width=True)

        if send:
            if query_request.is_url_correct is False:
                st.error("Неверная ссылка. Отправить отчет не удастся.")
            elif opio_name is None:
                st.warning("Необходимо выбрать название ОПиО")
            elif photo_need and photo_file is None:
                st.warning("Необходимо загрузить фото отчета без гашения")
            else:
                send_report(report_data, photo_need, photo_file, query_request, opio_name)


if __name__ == "__main__":
    main()