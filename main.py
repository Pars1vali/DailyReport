import streamlit as st
import logging
import bot, util
from service import form_service, report_service
from util import ConnectionQuery

logging.getLogger().setLevel(logging.INFO)

st.set_page_config(
    page_title="МегаФон",
)


def send_report(report: report_service.ReportMessage, connection_query: util.ConnectionQuery):
    if connection_query.is_url_correct is False:
        st.error("Неверная ссылка. Отправить отчет не удастся.")
    elif report.opio_name is None:
        st.warning("Необходимо выбрать название ОПиО")
    elif report.is_photo_need and report.photo_file is None:
        st.warning("Необходимо загрузить фото отчета без гашения")
    else:
        bot.send_report(report, connection_query)
        st.success("Отчет отправлен!")
        st.balloons()

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
        report.data = form_service.create_form(config)

        st.form_submit_button("Отправить", use_container_width=True, on_click=send_report,
                              args=[report, connection_query])


if __name__ == "__main__":
    main()
