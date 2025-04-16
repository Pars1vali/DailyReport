from pydoc_data.topics import topics

import streamlit as st
import uuid

variant_result = ["number", "credit", "money", "percent"]
variant_report = ["sales", "dopio"]

if "rows" not in st.session_state:
    st.session_state["rows"] = []

if "group" not in st.session_state:
    st.session_state["group"] = []

group_collection = []
rows_collection = []

def modify_type(option):
    label = option
    match option:
        case "number":
            label = "Колличество"
        case "money":
            label = "Стоимость"
        case "percent":
            label = "Проценты"
        case "credit":
            label = "Кредиты/БК"

    return label

def modify_type_report(option):
    label = option
    match option:
        case "sales":
            label = "Продажи"
        case "dopio":
            label = "Для руководителей"

    return label

def add_row():
    element_id = uuid.uuid4()
    st.session_state["rows"].append(str(element_id))

def add_group():
    element_id = uuid.uuid4()
    st.session_state["group"].append(str(element_id))

def remove_row(row_id):
    st.session_state["rows"].remove(str(row_id))

def remove_group(group_id):
    st.session_state["group"].remove(str(group_id))

def generate_group(group_id):
    group_container = st.empty()
    group_columns = group_container.columns((4,1))
    group_columns[1].button("🗑️", key=f"del_{group_id}", on_click=remove_group, args=[group_id])



def generate_row(row_id):
    row_container = st.empty()
    row_columns = row_container.columns((4, 3, 2, 2, 1))

    text = row_columns[0].text_input("Продажа", placeholder="Sim МегаФон+Yota, шт", key=f"txt_{row_id}")
    type_result = row_columns[1].selectbox("Измерение", options=variant_result, format_func=modify_type, key=f"type_{row_id}")
    have_plan = row_columns[2].checkbox("План/Факт", key=f"plan_fact_{row_id}")
    is_credit = row_columns[3].checkbox("Заявки/Одобрено/Выдано", key=f"credit_{row_id}")
    row_columns[4].button("🗑️", key=f"del_{row_id}", on_click=remove_row, args=[row_id])

    return {"text": text, "type": type_result, "have_plan": have_plan, "is_credit": is_credit}

st.header("Создание формы отчёта")
type_report = st.selectbox("Тип отчета", options=variant_report, format_func=modify_type_report, index=0)

for group in st.session_state["group"]:
    generate_group(group)
for row in st.session_state["rows"]:
    row_data = generate_row(row)
    rows_collection.append(row_data)

menu = st.columns(2)

with menu[0]:
    st.button("Добавить", on_click=add_row, type="primary")
with menu[1]:
    st.button("Добавить группу", on_click=add_group, type="primary")

send_data = st.button("Отправить", use_container_width=True)
if send_data:
    report_format = {
        "type_report": type_report,
        "topics": rows_collection
    }
    st.write(report_format)
