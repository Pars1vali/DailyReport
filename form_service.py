import streamlit as st



class Form:

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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
