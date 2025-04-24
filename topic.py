import streamlit as st

def credit(topic, index):
    text_topic = f'{topic["text"]} (заявки/одобрено/выдано)'
    emoji = topic.get("emoji", "🟢")
    st.markdown(f"**{text_topic}**")

    col1, col2, col3 = st.columns(3)
    with col1:
        loan_apply = st.number_input("Заявки", value=topic["unit"], min_value=topic["unit"],
                                     key=f"{index}loan_apply")
    with col2:
        approved = st.number_input("Одобрено", value=topic["unit"], min_value=topic["unit"],
                                   key=f"{index}approved")
    with col3:
        issued = st.number_input("Выдано", value=topic["unit"], min_value=topic["unit"],
                                 key=f"{index}issued")

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

def plan_fact(topic, index):
    text_topic = f'{topic["text"]} (план/факт)'
    emoji = topic.get("emoji", "🟢")
    st.markdown(f"**{text_topic}**")

    col1, col2 = st.columns(2)
    with col1:
        plan = st.number_input("План", value=topic["unit"], min_value=topic["unit"], key=f"{index}plan")
    with col2:
        fact = st.number_input("Факт", value=topic["unit"], min_value=topic["unit"], key=f"{index}fact")

    return {
        "text": text_topic,
        "emoji": emoji,
        "value": {
            "plan": plan,
            "fact": fact
        },
        "is_credit": False,
        "have_plan": True,
        "share": False
    }

def share(topic, index):
    text_topic = f'{topic["text"]} %'
    emoji = topic.get("emoji", "🟢")
    divisible_text = topic.get("divisible", "Число 1")
    divider_text = topic.get("divider", "Число 2")

    st.markdown(f"**{text_topic}**")
    col1, col2 = st.columns(2)
    with col1:
        divisible = st.number_input(divisible_text, value=topic["unit"], min_value=topic["unit"], key=f"{index}plan")
    with col2:
        divider = st.number_input(divider_text, value=topic["unit"], min_value=topic["unit"], key=f"{index}fact")

    share = int((divider * 100) / (divisible)) if divisible else 0
    return {
        "text": text_topic,
        "emoji": emoji,
        "value": {
            "divisible": divisible,
            "divider": divider,
            "share": share
        },
        "is_credit": False,
        "have_plan": False,
        "share": True
    }

def number(topic, index_group, index_topic):
    unit = "руб" if topic["type"] == "money" else "шт"
    text_topic = f'{topic["text"]}, {unit}'
    value_topic = st.number_input( text_topic, value=topic["unit"],
                                  min_value=topic["unit"], key=f"{index_group}_{index_topic}_number")
    emoji = topic.get("emoji", "🟢")

    return {
        "text": topic["text"],
        "emoji": emoji,
        "value": value_topic,
        "is_credit": False,
        "have_plan": False,
        "share": False
    }

