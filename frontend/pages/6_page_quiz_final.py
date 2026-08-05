from datetime import datetime

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

import api_client
from auth_utils import require_login, render_logout_sidebar
from styles import read_css, hide_streamlit_chrome

st.set_page_config(page_title="Результаты теста", page_icon="💻", layout="wide")
hide_streamlit_chrome()

button_style = read_css("button_style_ease.css")

require_login()

st.markdown("""
<style>
    .header { font-size: 28px; font-weight: bold; margin-bottom: 10px; }
    .subheader { font-size: 22px; font-weight: bold; margin-top: 20px; margin-bottom: 10px; }
    .performance-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    .performance-table th, .performance-table td { padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd; }
    .performance-table th { background-color: #f2f2f2; font-weight: normal; }
    .performance-table td { font-weight: bold; }
    .test-card { border: 1px solid #ddd; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .test-card:hover { box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
    .topic-tag { display: inline-block; padding: 3px 8px; background-color: #f0f0f0; border-radius: 4px; font-size: 0.8em; margin-right: 5px; margin-bottom: 5px; }
    .summary-title { font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #2c3e50; }
    .summary-item { margin-bottom: 12px; }
    .summary-label { font-size: 14px; color: #7f8c8d; }
    .summary-value { font-size: 16px; font-weight: bold; color: #2c3e50; margin-top: 3px; }
    .highlight-value { color: #4e79a7; font-weight: 800; }
    .summary-divider { border-top: 1px solid #e0e0e0; margin: 10px 0; }
    .stButton>button { border: 2px solid white; color: white; background-color: #4a6bdf; transition: all 0.3s ease; }
    .stButton>button:hover { border: 2px solid white; color: white; background-color: #3a5bcf; }
    .stButton>button:focus { border: 2px solid white; color: white; }
</style>
""", unsafe_allow_html=True)

if st.button("← Главная", key="home_button"):
    st.switch_page("home_page.py")

result = st.session_state.get("last_result")

if not result:
    st.info("Ты ещё не прошёл ни одного теста в этой сессии.")
    st.page_link("pages/4_page_select_test.py", label="Пройти тест", icon="📝")
    render_logout_sidebar()
    st.stop()

# Header
st.markdown('<div class="header">Результаты теста</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subheader">{result["subject"]}</div>', unsafe_allow_html=True)

main_col, summary_col = st.columns([3, 1])

with main_col:
    st.markdown(f"Тест выполнен {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    st.markdown("---")
    st.markdown("**Успех по темам**")

    rows = ""
    for theme, stats in result["by_theme"].items():
        pct = round(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        rows += f"<tr><th>{theme}</th><td>{pct}%</td></tr>"

    if rows:
        st.markdown(f'<table class="performance-table">{rows}</table>', unsafe_allow_html=True)
    else:
        st.write("Нет отвеченных вопросов.")

    st.markdown("---")
    st.markdown("### Рекомендации")
    st.markdown("Основываясь на твоей общей статистике, рекомендуем подтянуть следующие темы.")

    try:
        recommended = api_client.get_recommendations(limit=3)
    except api_client.ApiError:
        recommended = []

    if recommended:
        for theme in recommended:
            with st.container():
                st.markdown(f"""
                <div class="test-card">
                    <h3>{theme}</h3>
                    <span class="topic-tag">{theme}</span>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.write("Пока недостаточно данных для рекомендаций.")

    with stylable_container(key="retry_button", css_styles=button_style):
        action_cols = st.columns(3)
        with action_cols[0]:
            if st.button("Пройти ещё один тест", key="retry_btn", use_container_width=True):
                st.switch_page("pages/4_page_select_test.py")
        with action_cols[1]:
            if st.button("Добавить вопрос", key="add_question_btn", use_container_width=True):
                st.switch_page("pages/7_page_create_test.py")
        with action_cols[2]:
            if st.button("На главную", key="home_btn_bottom", use_container_width=True):
                st.switch_page("home_page.py")

with summary_col:
    score_pct = round(100 * result["correct"] / result["answered"]) if result["answered"] else 0
    minutes, seconds = divmod(result["time_spent"], 60)
    st.markdown(f"""
    <div class="test-card">
        <div class="summary-title">Результаты теста</div>
        <div class="summary-item">
            <div class="summary-label">Потраченное время</div>
            <div class="summary-value highlight-value">{minutes} мин {seconds} сек</div>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
            <div class="summary-label">Правильных ответов</div>
            <div class="summary-value highlight-value">{result["correct"]} из {result["answered"]} ({score_pct}%)</div>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
            <div class="summary-label">Всего вопросов в тесте</div>
            <div class="summary-value">{result["total_questions"]}</div>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
            <div class="summary-label">Предмет</div>
            <div class="summary-value">{result["subject"]}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

render_logout_sidebar()
