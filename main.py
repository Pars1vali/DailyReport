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


def create_form(config_report):
    form_data = list()

    for section in config_report["schema"]:
        section_data = list()

        for topic in section:
            if topic["is_credit"] is True:
                topic_data = form_service.create_credit_topic(topic)
            elif topic["have_plan"] is True:
                topic_data = form_service.create_plan_fact_topic(topic)
            elif topic["share"] is True:
                topic_data = form_service.create_share_topic(topic)
            else:
                topic_data = form_service.create_number_topic(topic)

            section_data.append(topic_data)

        form_data.append(section_data)
    st.write(form_data)
    return form_data


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
        report.data = create_form(config)

        send_report_btn = st.form_submit_button("Отправить", use_container_width=True)

        if send_report_btn:
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
