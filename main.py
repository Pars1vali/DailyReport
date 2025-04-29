import streamlit as st
import logging
import bot, util
import report_service
import form_service
from util import ConnectionQuery

logging.getLogger().setLevel(logging.INFO)

st.set_page_config(
    page_title="МегаФон",
)

report_data = list()


def create_credit_topic(topic: dict) -> dict:
    topic_text = f'{topic["text"]} (заявки/одобрено/выдано)'
    emoji = topic.get("emoji", "🟢")
    help = topic.get("help", None)
    st.markdown(f"**{topic_text}**")

    col1, col2, col3 = st.columns(3)
    with col1:
        loan_apply = st.number_input("Заявки", value=topic["unit"], min_value=topic["unit"], help=help,
                                     placeholder=help,
                                     key=f"{id(topic)}loan_apply")
    with col2:
        approved = st.number_input("Одобрено", value=topic["unit"], min_value=topic["unit"], help=help,
                                   placeholder=help,
                                   key=f"{id(topic)}approved")
    with col3:
        issued = st.number_input("Выдано", value=topic["unit"], min_value=topic["unit"], help=help,
                                 placeholder=help,
                                 key=f"{id(topic)}issued")

    return {
        "text": topic_text,
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

def create_plan_fact_topic(topic: dict) -> dict:
    topic_text = f'{topic["text"]} (план/факт)'
    emoji = topic.get("emoji", "🟢")
    help = topic.get("help", None)

    st.markdown(f"**{topic_text}**")

    col1, col2 = st.columns(2)
    with col1:
        plan = st.number_input("План", value=topic["unit"], min_value=topic["unit"], help=help, placeholder=help,
                               key=f"{id(topic)}plan")
    with col2:
        fact = st.number_input("Факт", value=topic["unit"], min_value=topic["unit"], help=help, placeholder=help,
                               key=f"{id(topic)}fact")

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

def create_share_topic(topic: dict) -> dict:
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
                                    key=f"{id(topic)}plan")
    with col2:
        divider = st.number_input(divider_text, value=topic["unit"], min_value=topic["unit"], help=help,
                                  placeholder=help,
                                  key=f"{id(topic)}fact")

    share_value = int((divider * 100) / (divisible)) if divisible else 0
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

def create_number_topic(topic: dict) -> dict:
    topic_type = topic.get("type", "number")
    unit_name = "руб." if topic_type == "money" else "шт."
    unit_value = topic.get("unit", 0)
    topic_text = f'{topic["text"]}, {unit_name}'
    emoji = topic.get("emoji", "🟢")
    help = topic.get("help", None)

    value_topic = st.number_input(topic_text,
                                  value=unit_value,
                                  min_value=unit_value,
                                  help=help, placeholder=help,
                                  key=f"{id(topic)}_number")

    return {
        "text": topic_text,
        "emoji": emoji,
        "value": value_topic,
        "is_credit": False,
        "have_plan": False,
        "share": False
    }


def main():
    connection_query = ConnectionQuery.create(st.query_params)
    config = report_service.get_config(connection_query)

    report = report_service.ReportMessage()
    report.name = config.get("name", "Отчет")
    report.is_photo_need = config.get("photo_need", False)

    with st.form("Отчет"):
        st.subheader(report.name)

        report.opio_name = st.selectbox("Название вашего ОПиО", util.get_opio_list(), index=None, placeholder="ОПиО")
        report.photo_file = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])

        for section in config["schema"]:
            section_data = list()

            for topic in section:
                if topic["is_credit"] is True:
                    topic_data = create_credit_topic(topic)
                elif topic["have_plan"] is True:
                    topic_data = create_plan_fact_topic(topic)
                elif topic["share"] is True:
                    topic_data = create_share_topic(topic)
                else:
                    topic_data = create_number_topic(topic)

                section_data.append(topic_data)
            report_data.append(section_data)

        report.data = report_data
        send_report_btn = st.form_submit_button("Отправить", use_container_width=True)

        if send_report_btn:
            st.write(report.data)
            if connection_query.is_url_correct is False:
                st.error("Неверная ссылка. Отправить отчет не удастся.")
            elif report.opio_name is None:
                st.warning("Необходимо выбрать название ОПиО")
            elif report.is_photo_need and report.photo_file is None:
                st.warning("Необходимо загрузить фото отчета без гашения")
            else:
                bot.send_report(report, connection_query)


if __name__ == "__main__":
    main()
