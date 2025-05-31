import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go
import pandas as pd

# Page configuration
st.set_page_config(page_title="Главная", page_icon="💻", layout="wide")

# Custom CSS for styling
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
</style>
""", unsafe_allow_html=True)

# Header
st.title("Добро пожаловать!")
st.subheader("Продолжай свой путь в изучении информатики")

# Metrics row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Тестов выполнено", value="12", delta="+2 с прошлой недели")
with col2:
    st.metric(label="Среднее выполнение", value="82%", delta="+5% повышения")
with col3:
    st.metric(label="Время в тренажере", value="24h", delta="В этом месяце")

style_metric_cards()

# Main content columns
col_left, col_right = st.columns([2, 1])

with col_left:
    # Recent Test Results section
    st.header("Recent Test Results")
    st.caption("Your latest performance overview")
    
    # Test items with checkboxes
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
    
    
    # Quick Actions
    st.header("Быстрые действия")
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        if st.button("Начать тест", use_container_width=True):
            st.session_state.action = "new_test"
    with action_col2:
        if st.button("Создать новый", use_container_width=True):
            st.session_state.action = "create_test"
    with action_col3:
        if st.button("Посмотреть аналитику", use_container_width=True):
            st.session_state.action = "analytics"

with col_right:
    # Learning Progress
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
    
