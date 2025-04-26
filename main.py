import streamlit as st
import logging
import bot, opio, form
from opio import QueryRequest

logging.getLogger().setLevel(logging.INFO)

st.set_page_config(
        page_title="МегаФон",
)

def main():
    query_request = QueryRequest.create(st.query_params)
    config_report = opio.get_report_config(query_request)

    photo_need = config_report.get("photo_need", False)
    name_report = config_report.get("name", "Отчет")

    with st.form("Отчет"):
        st.subheader(name_report)
        opio_name = st.selectbox("Название вашего ОПиО", opio.get_opio_list(), index=None, placeholder="ОПиО")
        photo_file = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])

        report_data = form.create_form(config_report)

        send = st.form_submit_button("Отправить", use_container_width=True)

        if send:
            if query_request.is_url_correct is False:
                st.error("Неверная ссылка. Отправить отчет не удастся.")
            elif opio_name is None:
                st.warning("Необходимо выбрать название ОПиО")
            elif photo_need and photo_file is None:
                st.warning("Необходимо загрузить фото отчета без гашения")
            else:
                bot.send_report(report_data, photo_need, photo_file, query_request, opio_name)
                st.success("Отчет отправлен!")
                st.balloons()

if __name__ == "__main__":
    main()