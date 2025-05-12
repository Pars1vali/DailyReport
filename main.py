import json
import streamlit as st
import logging
import sales
import util, bot
from util import get_opio_list

logging.getLogger().setLevel(logging.INFO)

def create_plan_fact_topic(topic: dict, index_topic: int) -> dict:
    topic_text = f'{topic["text"]} (план/факт)'
    emoji = topic.get("emoji", "🟢")
    help = topic.get("help", None)

    st.markdown(f"**{topic_text}**")

    col1, col2 = st.columns(2)
    with col1:
        plan = st.number_input("План", value=topic["unit"], min_value=topic["unit"], help=help, placeholder=help,
                               key=f"{index_topic}plan")
    with col2:
        fact = st.number_input("Факт", value=topic["unit"], min_value=topic["unit"], help=help, placeholder=help,
                               key=f"{index_topic}fact")

    return {
        "text": topic_text,
        "emoji": emoji,
        "value": {
            "plan": plan,
            "fact": fact
        },
        "is_credit": False,
        "have_plan": True,
        "share": False
    }

def create_share_topic(topic: dict, index_topic: int) -> dict:
    topic_text = f'{topic["text"]} %'
    emoji = topic.get("emoji", "🟢")
    help = topic.get("help", None)
    divisible_text = topic.get("divisible", "Число 1")
    divider_text = topic.get("divider", "Число 2")

    st.markdown(f"**{topic_text}**")
    col1, col2 = st.columns(2)
    with col1:
        divisible = st.number_input(divisible_text, value=topic["unit"], min_value=topic["unit"], help=help,
                                    placeholder=help,
                                    key=f"{index_topic}plan")
    with col2:
        divider = st.number_input(divider_text, value=topic["unit"], min_value=topic["unit"], help=help,
                                  placeholder=help,
                                  key=f"{index_topic}fact")

    share_value = int(divider / divisible * 100) if divisible else 0
    return {
        "text": topic_text,
        "emoji": emoji,
        "value": {
            "divisible": divisible,
            "divider": divider,
            "share": share_value
        },
        "is_credit": False,
        "have_plan": False,
        "share": True
    }

def create_credit_topic(topic, index_topic: int) -> dict:
    text_topic = f'{topic["text"]} (подано/одобрено/выдано)'
    emoji = topic.get("emoji", "🟢")

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
        "emoji": emoji,
        "value": {
            "loan_apply": loan_apply,
            "approved": approved,
            "issued": issued
        },
        "is_credit": True,
        "have_plan": False,
        "share": False
    }

def create_number_topic(topic: dict) -> dict:
    unit_text_topic = "руб." if topic["type"] == "money" else "шт."
    text_topic = f'{topic["text"]} {unit_text_topic}'
    value_topic = st.number_input(topic["text"], value=topic["unit"],
                                  min_value=topic["unit"])
    emoji = topic.get("emoji", "🟢")

    return {
        "text": text_topic,
        "emoji": emoji,
        "value": value_topic,
        "is_credit": False,
        "have_plan": False,
        "share": False
    }

def get_query_info():
    try:
        query_report = util.ConnectionQuery(is_url_correct=True)
        query_report.report_type = st.query_params["report_type"]
        query_report.chat_id = st.query_params["chat_id"]
        query_report.report_id = st.query_params["report_id"]
        query_report.sales_id = st.query_params["sales_id"]
    except Exception as e:
        query_report.is_url_correct = False
        query_report.report_type = "sales"
        logging.error(f"Error for get query params from url-request. Send report impossible. {e}")

    return query_report

def get_model_report(query_report: util.ConnectionQuery):
    if query_report.report_type == "dopio":
        src_path = "src/model/dopio.json"
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
        photo_need = model_report.get("photo_need", False)

        report_data = list()

        for index_group, group in enumerate(model_report["schema"]):
            report_group = list()

            for index_topic, topic in enumerate(group):
                if topic["is_credit"] is True:
                    report_topic = create_credit_topic(topic, index_topic)
                elif topic["have_plan"] is True:
                    report_topic = create_plan_fact_topic(topic, index_topic)
                elif topic["share"] is True:
                    report_topic = create_share_topic(topic, index_topic)
                else:
                    report_topic = create_number_topic(topic)

                report_group.append(report_topic)

            report_data.append(report_group)

        send = st.form_submit_button("Отправить", use_container_width=True)

        if send:
            if query_report.is_url_correct is False:
                st.error("Неверная ссылка. Отправить отчет не удастся.")
            elif opio_name is None:
                st.warning("Необходимо выбрать название ОПиО")
            elif photo_need and photo_cheque is None:
                st.warning("Необходимо загрузить фото отчета без гашения")
            else:
                with st.status("Отчет отправляется..."):
                    bot.send_report(report_data, photo_need, photo_cheque, query_report, opio_name)
                    st.write("Отчет отправлен.")
                    st.write("Подсчет продаж...")
                    sales_data = sales.calc(report_data, query_report)
                    sales_message = sales.create_sales_message(sales_data)
                    bot.send_sales_message(sales_message, query_report)
                    st.success("Готово!")
                    # st.success("Отчет отправлен!")
                    st.balloons()


if __name__ == "__main__":
    main()