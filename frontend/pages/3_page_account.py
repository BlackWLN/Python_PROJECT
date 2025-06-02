import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
import pandas as pd

from streamlit_extras.stylable_container import stylable_container

with open("button_style_ease.css") as b:
    button_style = b.read()

st.set_page_config(page_title="Главная", page_icon="💻", layout="wide")

st.markdown("""
<style>
    .st-emotion-cache-1y4p8pa {
        padding: 2rem 1rem;
    }
    .test-item {
        padding: 0.5rem 0;
        border-bottom: 1px solid #eee;
    }
    .progress-container {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 15px;
    }
    .progress-bar {
        height: 10px;
        border-radius: 5px;
        background-color: #e0e0e0;
        margin-top: 5px;
    }
    .progress-fill {
        height: 100%;
        border-radius: 5px;
        background-color: #4CAF50;
    }
    .achievement-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
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

st.markdown(
        """
        <div class="home-button">
            <a href="/" target="_self">
                <button style="background-color: #f0f0f0; color: black; border: 1px solid #ddd; padding: 8px 16px; border-radius: 4px; cursor: pointer;">
                    ←  Главная
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

# Header
st.title("Добро пожаловать!")
st.subheader("Продолжай свой путь в изучении информатики")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Тестов выполнено", value="12", delta="+2 с прошлой недели")
with col2:
    st.metric(label="Среднее выполнение", value="82%", delta="+5% повышения")
with col3:
    st.metric(label="Время в тренажере", value="24h", delta="В этом месяце")

style_metric_cards()

# Main
col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("Недавние результаты")
    st.caption("Просмотр ваших послежних успехов")
    st.markdown("""
    <div class="test-item">
        <input type="checkbox" disabled> <strong>Основы структур данных</strong><br>
        <span style="color: #666;">2 days ago</span>
    </div>
    <div class="test-item">
        <input type="checkbox" disabled> <strong>Анализ алгоритмов</strong><br>
        <span style="color: #666;">1 week ago</span>
    </div>
    <div class="test-item">
        <input type="checkbox" disabled> <strong>Что-нибудь еще</strong><br>
        <span style="color: #666;">2 weeks ago</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.header("Быстрые действия")
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button("Начать тест", use_container_width=True, type="primary"):
            st.session_state.action = "new_test"
    with action_col2:
        if st.button("Создать новый", use_container_width=True, type="primary"):
            st.session_state.action = "create_test"

    with stylable_container(
        key="get_started_button",
        css_styles=button_style,
    ):
        st.button("Посмотреть аналитику", key="review_btn")

with col_right:
    st.header("Прогресс в обучении")
    st.caption("Ваш общий прогресс в этом месяце")
    
    progress_data = {
        "Topic": ["Алгоритмы", "Структуры данных", "Анализ сложности"],
        "Progress": [75, 60, 85]
    }
    
    for topic, progress in zip(progress_data["Topic"], progress_data["Progress"]):
        st.markdown(f"""
        <div class="progress-container">
            <div style="display: flex; justify-content: space-between;">
                <span><strong>{topic}</strong></span>
                <span>{progress}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
