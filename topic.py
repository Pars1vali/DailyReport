import streamlit as st

def credit_topic(topic, index_topic):
    text_topic = topic["text"]
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
        "have_plan": False
    }

def plan_fact_topic(topic, index_group):
    text_topic = topic["text"]
    emoji = topic.get("emoji", "🟢")
    st.markdown(f"**{text_topic}**")

    col1, col2 = st.columns(2)
    with col1:
        plan = st.number_input("План", value=topic["unit"], min_value=topic["unit"], key=f"{index_group}plan")
    with col2:
        fact = st.number_input("Факт", value=topic["unit"], min_value=topic["unit"], key=f"{index_group}fact")

    return {
        "text": text_topic,
        "emoji": emoji,
        "value": {
            "plan": plan,
            "fact": fact
        },
        "is_credit": False,
        "have_plan": True
    }

def number_topic(topic, index_group, index_topic):
    value_topic = st.number_input(topic["text"], value=topic["unit"],
                                  min_value=topic["unit"], key=f"{index_group}_{index_topic}_number")
    emoji = topic.get("emoji", "🟢")

    return {
        "text": topic["text"],
        "emoji": emoji,
        "value": value_topic,
        "is_credit": False,
        "have_plan": False
    }