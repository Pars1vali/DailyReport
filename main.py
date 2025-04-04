import streamlit as st
import group
from group import group_topics, opio_list

form = dict()

def credit_topic(topic: group.Topic):
    st.markdown(f"**{topic.text}**")

    col1, col2, col3 = st.columns(3)
    with col1:
        loan_apply = st.number_input("Заявки", value=topic.unit, min_value=topic.unit, key=f"{index_topic}loan_apply")
    with col2:
        approved = st.number_input("Одобрено", value=topic.unit, min_value=topic.unit, key=f"{index_topic}approved")
    with col3:
        issued = st.number_input("Выдано", value=topic.unit, min_value=topic.unit, key=f"{index_topic}issued")

    form[topic.text] = {
        "Заявки": loan_apply,
        "Одобрено": approved,
        "Выдано": issued
    }

def plan_fact_topic(topic: group.Topic):
    st.markdown(f"**{topic.text}**")

    col1, col2 = st.columns(2)
    with col1:
        plan = st.number_input("План", value=topic.unit, min_value=topic.unit, key=f"{index_group}plan")
    with col2:
        fact = st.number_input("Факт", value=topic.unit, min_value=topic.unit, key=f"{index_group}fact")

    form[topic.text] = {
        "План": plan,
        "Факт": fact
    }

with st.form("Отчет"):

    opio_name = st.selectbox("Название вашего ОПиО", opio_list, index=None, placeholder="ОПиО")
    photo_cheque = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])

    form["Название ОПиО"] = opio_name

    for index_group, group in enumerate(group_topics):

        st.divider()
        for index_topic, topic in enumerate(group.topics):

            if topic.is_credit:
                credit_topic(topic)
            elif topic.have_plan:
                plan_fact_topic(topic)
            else:
                form[topic.text] = st.number_input(topic.text, value=topic.unit, min_value=topic.unit)

    send = st.form_submit_button("Отправить", use_container_width=True)

if send and opio_name is not None:
    st.write(form)
    st.write("Verison 1")

    st.html("""
        <head>
        <script src="https://telegram.org/js/telegram-web-app.js?56"></script>
        </head>
        
        <script>
        let tg = window.Telegram.WebApp;
        tg.sendData("data");
        tg.close();
        </script>
    """)

