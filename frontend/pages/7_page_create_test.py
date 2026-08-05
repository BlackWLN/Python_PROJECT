import streamlit as st
from streamlit_extras.stylable_container import stylable_container

import api_client
from auth_utils import require_login, render_logout_sidebar
from styles import read_css, hide_streamlit_chrome

st.set_page_config(page_title="Создать тест", page_icon="💻", layout="wide")
hide_streamlit_chrome()

button_style = read_css("button_style_ease.css")

require_login()

st.markdown("""
    <style>
        .stButton>button {
            border: 2px solid white;
            color: white;
            background-color: #4a6bdf;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            border: 2px solid white;
            color: white;
            background-color: #3a5bcf;
        }
        .stButton>button:focus {
            border: 2px solid white;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

if st.button("← Главная", key="home_button"):
    st.switch_page("home_page.py")

st.title("Добавить вопрос")
st.subheader("Предложи свой вопрос — он попадёт в общий банк вопросов и станет доступен всем, кто проходит тест по этой теме")

try:
    subjects = api_client.get_subjects()
except api_client.ApiError as exc:
    st.error(f"Не удалось загрузить существующие предметы: {exc}")
    subjects = []

subject_names = [s["subject"] for s in subjects]
themes_by_subject = {s["subject"]: s["themes"] for s in subjects}

NEW_OPTION = "+ Новый предмет"

with st.form("question_form"):
    subject_choice = st.selectbox("Предмет", subject_names + [NEW_OPTION])
    if subject_choice == NEW_OPTION:
        subject = st.text_input("Название нового предмета", placeholder="Например: ФИ")
        theme = st.text_input("Тема", placeholder="Например: Кодирование")
    else:
        subject = subject_choice
        existing_themes = themes_by_subject.get(subject, [])
        theme_choice = st.selectbox("Тема", existing_themes + ["+ Новая тема"])
        theme = st.text_input("Название новой темы") if theme_choice == "+ Новая тема" else theme_choice

    question_text = st.text_area("Вопрос", placeholder="Введи текст вопроса")

    st.markdown("**Варианты ответа** (заполни минимум 2, отметь правильный)")
    option_cols = st.columns(2)
    options = []
    for i in range(4):
        with option_cols[i % 2]:
            option = st.text_input(f"Вариант {i + 1}", key=f"option_{i}", placeholder=f"Вариант {i + 1}")
            options.append(option)

    non_empty_indices = [i for i, o in enumerate(options) if o.strip()]
    correct_label = st.radio(
        "Правильный ответ",
        options=[f"Вариант {i + 1}" for i in non_empty_indices] or ["Заполни варианты выше"],
    )

    submitted = st.form_submit_button("Сохранить вопрос", type="primary")

    if submitted:
        if not subject or not subject.strip():
            st.error("Укажи предмет")
        elif not theme or not theme.strip():
            st.error("Укажи тему")
        elif not question_text or not question_text.strip():
            st.error("Введи текст вопроса")
        elif len(non_empty_indices) < 2:
            st.error("Заполни хотя бы 2 варианта ответа")
        else:
            correct_idx = int(correct_label.split()[-1]) - 1
            answers_payload = [
                {"answer_text": options[i].strip(), "is_correct": i == correct_idx}
                for i in non_empty_indices
            ]
            try:
                created = api_client.create_question(
                    question_text=question_text.strip(),
                    theme=theme.strip(),
                    subject=subject.strip(),
                    answers=answers_payload,
                )
                st.success(f"Вопрос добавлен в тему «{created['theme']}»!")
                st.page_link("pages/4_page_select_test.py", label="Пройти тест по этой теме", icon="📝")
            except api_client.ApiError as exc:
                st.error(f"Не удалось сохранить вопрос: {exc}")

render_logout_sidebar()
