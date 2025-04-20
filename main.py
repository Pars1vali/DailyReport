import json
import streamlit as st
import logging
import bot, group
import report
from group import opio_list, char_complete_opio

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
        query_report = group.QueryReport(url_correct=True)
        query_report.type_report = st.query_params["type_report"]
        query_report.chat_id = st.query_params["chat_id"]
        query_report.message_id = st.query_params["message_id"]
    except Exception as e:
        query_report.url_correct = False
        logging.error(e)

    return query_report


def main():
    query_report = get_query_info()

    with open('report_daily.json', encoding='utf-8') as file:
        data = json.load(file)

    with st.form("Отчет"):
        st.header("Отчет")
        opio_name = st.selectbox("Название вашего ОПиО", opio_list, index=None, placeholder="ОПиО")
        photo_cheque = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])

        for index_group, group in enumerate(data["topics"]):
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