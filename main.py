import streamlit as st

class GroupTopic:
    def __init__(self, topics: list):
        self.topics = topics

class Topic:

    def __init__(self, text: str, unit, is_credit:bool = False, have_plan:bool = False):
        self.text = text
        self.unit = unit
        self.is_credit = is_credit
        self.have_plan = have_plan


group_topics = list([
    GroupTopic([
        Topic("Сим Мегафон+Yota, шт",0),
        Topic("Мегасемья",0)
    ]),
    GroupTopic([
        Topic("Абонементы мегафон +ета",0, have_plan=True),
        Topic("Доля абонементов от сим",0.0)
    ]),
    GroupTopic([
        Topic("РК REALME(модели по акции)",0),
        Topic("РК HONOR(модели по акции)",0),
        Topic("Первая цена",0),
        Topic("Хуавей",0),
        Topic("Apple",0)
    ]),
    GroupTopic([
        Topic("Аксесуары",0.0),
        Topic("Акция 1+1",0.0)
    ]),
    GroupTopic([
        Topic("ФУ",0.0),
        Topic("Плотер",0),
        Topic("Страховки",0.0),
    ]),
    GroupTopic([
        Topic("КД заявки шт / одобрено шт /выдано шт",0, is_credit=True),
        Topic("БК заявки шт / одобрено шт / выдано шт",0, is_credit=True)
    ]),
    GroupTopic([
        Topic("Адаптер",0)
    ]),
    GroupTopic([
        Topic("NPS 9/10 факт за день", 0)
    ])
])

opio_list = list([
    "Став 189",
    "Став 141",
    "Став/Веш",
    "Лента",
    "Оз",
    "Мачуги",
    "Игнатова",
    "Сормовская",
    "Тюляева",
    "Новомих",
    "Гулькевичи",
    "Туапсе Маркса",
    "Туапсе Жукова",
    "Кропоткин 226",
    "Кропоткин 72",
    "Усть-Лабинск Ленина",
    "Усть-Лабинск Ободовского"
])

form = dict()

with st.form("Отчет"):

    opio_name = st.selectbox("Название вашего ОПиО", opio_list, index=None, placeholder="ОПиО")
    photo_cheque = st.file_uploader("Отчет без гашения")

    form["Название ОПиО"] = opio_name

    for index_group, group in enumerate(group_topics):

        st.divider()
        for index_topic, topic in enumerate(group.topics):

            if topic.is_credit:
                st.markdown(f"**{topic.text}**")

                col1, col2, col3 = st.columns(3)
                with col1:
                    loan_apply = st.number_input("Заявки", value=topic.unit, key=f"{index_topic}loan_apply")
                with col2:
                    approved = st.number_input("Одобрено", value=topic.unit, key=f"{index_topic}approved")
                with col3:
                    issued = st.number_input("Выдано", value=topic.unit, key=f"{index_topic}issued")

                form[topic.text] = {
                    "Заявки": loan_apply,
                    "Одобрено": approved,
                    "Выдано": issued
                }

            elif topic.have_plan:
                st.markdown(f"**{topic.text}**")

                col1, col2 = st.columns(2)
                with col1:
                    plan = st.number_input("План", value=topic.unit, key=f"{index_group}plan")
                with col2:
                    fact = st.number_input("Факт", value=topic.unit, key=f"{index_group}fact")

                form[topic.text] = {
                    "План": plan,
                    "Факт": fact
                }
            else:
                form[topic.text] = st.number_input(topic.text, value=topic.unit)

    send = st.form_submit_button("Отправить")

if send and opio_name is not None:
    st.write(form)

