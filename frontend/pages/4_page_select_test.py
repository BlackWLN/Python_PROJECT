import streamlit as st
from streamlit_extras.stylable_container import stylable_container

import api_client
from auth_utils import require_login, render_logout_sidebar
from styles import read_css, hide_streamlit_chrome

st.set_page_config(page_title="Выбрать тест", page_icon="💻", layout="wide")
hide_streamlit_chrome()

button_style = read_css("button_style.css")

require_login()

# Custom CSS for styling
st.markdown("""
<style>
    .test-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .test-card:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .topic-tag {
        display: inline-block;
        padding: 3px 8px;
        background-color: #f0f0f0;
        border-radius: 4px;
        font-size: 0.8em;
        margin-right: 5px;
        margin-bottom: 5px;
    }
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

st.markdown(
    '<div style="display:flex; align-items:baseline; gap:12px; flex-wrap:wrap;">'
    '<span style="font-size:2rem; font-weight:700;">Доступные тесты</span>'
    '<span style="font-size:1rem; color:#666;">Выбери предмет и темы, по которым хочешь пройти тестирование</span>'
    '</div>',
    unsafe_allow_html=True
)

try:
    subjects = api_client.get_subjects()
except api_client.ApiError as exc:
    st.error(f"Не удалось загрузить список тем: {exc}")
    subjects = []

if not subjects:
    st.info("В базе пока нет вопросов. Добавь свой первый вопрос на странице «Создать тест».")
    st.page_link("pages/7_page_create_test.py", label="Создать вопрос", icon="➕")
    render_logout_sidebar()
    st.stop()

subject_names = [s["subject"] for s in subjects]
themes_by_subject = {s["subject"]: s["themes"] for s in subjects}

# Рекомендованные темы на основе статистики пользователя
try:
    recommended = api_client.get_recommendations(limit=3)
except api_client.ApiError:
    recommended = []

if recommended:
    st.markdown(
        '<div style="display:flex; align-items:baseline; gap:12px; flex-wrap:wrap; margin-top:1rem;">'
        '<span style="font-size:1.5rem; font-weight:700;">Рекомендованные темы</span>'
        '<span style="font-size:0.9rem; color:#666;">Основано на твоих прошлых результатах '
        '(или на самых больших темах, если ты ещё не проходил тесты)</span>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        "".join(f'<span class="topic-tag">{t}</span>' for t in recommended),
        unsafe_allow_html=True
    )

st.header("Настрой тест")

selected_subject = st.selectbox("Предмет", subject_names, key="select_subject")
available_themes = themes_by_subject.get(selected_subject, [])

selected_themes = st.multiselect(
    "Темы",
    available_themes,
    default=available_themes,
    placeholder="Выбери одну или несколько тем",
    key="select_themes"
)

col1, col2 = st.columns(2)
with col1:
    question_count = st.number_input(
        "Максимум вопросов", min_value=1, max_value=50, value=10, step=1
    )
with col2:
    time_limit_minutes = st.number_input(
        "Лимит времени (минут, 0 = без ограничения)", min_value=0, max_value=180, value=15, step=5
    )

with stylable_container(key="start_test_button", css_styles=button_style):
    start_clicked = st.button("Начать тест", type="primary", use_container_width=True)

if start_clicked:
    if not selected_themes:
        st.error("Выбери хотя бы одну тему")
    else:
        st.session_state["quiz_config"] = {
            "subject": selected_subject,
            "themes": selected_themes,
            "question_count": int(question_count),
            "time_limit": int(time_limit_minutes) * 60 if time_limit_minutes else None,
        }
        # Сбрасываем состояние предыдущего прохождения теста
        for key in ("quiz_questions", "current_question", "answers", "question_status",
                    "start_time", "question_start_time", "last_result"):
            st.session_state.pop(key, None)
        st.switch_page("pages/5_page_quiz.py")

st.divider()
with stylable_container(key="create_test_button", css_styles=button_style):
    if st.button("Добавить свой вопрос", use_container_width=True):
        st.switch_page("pages/7_page_create_test.py")

render_logout_sidebar()
