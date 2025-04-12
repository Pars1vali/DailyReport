import streamlit as st
import logging
import bot
import group
from group import group_topics, opio_list

form = dict()
logging.getLogger().setLevel(logging.INFO)


def credit_topic(topic: group.Topic, index_topic):
    st.markdown(f"**{topic.text}**")

    col1, col2, col3 = st.columns(3)
    with col1:
        loan_apply = st.number_input("Заявки", value=topic.unit, min_value=topic.unit, key=f"{index_topic}loan_apply")
    with col2:
        approved = st.number_input("Одобрено", value=topic.unit, min_value=topic.unit, key=f"{index_topic}approved")
    with col3:
        issued = st.number_input("Выдано", value=topic.unit, min_value=topic.unit, key=f"{index_topic}issued")

    topic.value.credit = group.CreditValue(loan_apply, approved, issued)

    form[topic.text] = {
        "Заявки": loan_apply,
        "Одобрено": approved,
        "Выдано": issued
    }


def plan_fact_topic(topic: group.Topic, index_group):
    st.markdown(f"**{topic.text}**")

    col1, col2 = st.columns(2)
    with col1:
        plan = st.number_input("План", value=topic.unit, min_value=topic.unit, key=f"{index_group}plan")
    with col2:
        fact = st.number_input("Факт", value=topic.unit, min_value=topic.unit, key=f"{index_group}fact")

    topic.value.plan_fact = group.PlanFactValue(plan, fact)

    form[topic.text] = {
        "План": plan,
        "Факт": fact
    }


def make_message_report(opio_name: str, group_topics):
    message_report = f"🟢🟢🟣\nОфис - {opio_name}\n"
    for group in group_topics:
        message_report += "---\n"
        for topic in group.topics:
            if topic.have_plan:
                message_report += f"{topic.text} (план/факт) - {topic.value.plan_fact.plan}/{topic.value.plan_fact.fact}\n"
            elif topic.is_credit:
                message_report += f"{topic.text} (заявки/одобрено/выдано) - {topic.value.credit.loan_apply}/{topic.value.credit.approved}/{topic.value.credit.issued}\n"
            else:
                message_report += f"{topic.text} - {topic.value.number}\n"
    return message_report


def main():
    with st.form("Отчет"):
        opio_name = st.selectbox("Название вашего ОПиО", opio_list, index=None, placeholder="ОПиО")
        photo_cheque = st.file_uploader("Отчет без гашения", type=["jpg", "jpeg", "png"])

        form["Название ОПиО"] = opio_name

        for index_group, group in enumerate(group_topics):

            st.divider()
            for index_topic, topic in enumerate(group.topics):

                if topic.is_credit:
                    credit_topic(topic, index_topic)
                elif topic.have_plan:
                    plan_fact_topic(topic, index_group)
                else:
                    topic.value.number = st.number_input(topic.text, value=topic.unit, min_value=topic.unit)
                    form[topic.text] = topic.value.number

        send = st.form_submit_button("Отправить", use_container_width=True)

        if send and opio_name is not None and photo_cheque is not None:
            # st.write(form)
            message_report = make_message_report(opio_name, group_topics)
            bot.send_report(message_report, photo_cheque)
            st.success("Отчет отправлен!")
            st.balloons()


if __name__ == "__main__":
    main()
