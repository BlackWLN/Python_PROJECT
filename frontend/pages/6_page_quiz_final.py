import streamlit as st
from datetime import datetime
from streamlit_extras.stylable_container import stylable_container


with open("button_style_ease.css") as b:
    button_style = b.read()

st.set_page_config(page_title="Результаты теста", page_icon="💻", layout="wide")

st.markdown("""
<style>
    .header {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subheader {
        font-size: 22px;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .performance-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    .performance-table th, .performance-table td {
        padding: 8px 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    .performance-table th {
        background-color: #f2f2f2;
        font-weight: normal;
    }
    .performance-table td {
        font-weight: bold;
    }
    .recommendation-card {
        border-left: 4px solid #4e79a7;
        padding: 15px;
        margin: 15px 0;
        background-color: #f8f9fa;
        border-radius: 0 8px 8px 0;
    }
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
    .difficulty-tag {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        margin-right: 5px;
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
    .summary-title {
        font-size: 18px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #2c3e50;
    }
    .summary-item {
        margin-bottom: 12px;
    }
    .summary-label {
        font-size: 14px;
        color: #7f8c8d;
    }
    .summary-value {
        font-size: 16px;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 3px;
    }
    .highlight-value {
        color: #4e79a7;
        font-weight: 800;
    }
    .summary-divider {
        border-top: 1px solid #e0e0e0;
        margin: 10px 0;
    }
    .divider {
        border-top: 1px solid #e0e0e0;
        margin: 10px 0;
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
st.markdown('<div class="header">Результаты теста</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Название теста</div>', unsafe_allow_html=True)

# Main
main_col, summary_col = st.columns([3, 1])

with main_col:
    st.markdown(f"Тест выполнен {datetime.now().strftime('%d.%m.%Y')}")
    st.markdown("---")
    st.markdown("**Успех по темам**")
    
    performance_html = """
    <table class="performance-table">
        <tr>
            <th>Структуры данных</th>
            <td>75%</td>
        </tr>
        <tr>
            <th>Алгоритмы</th>
            <td>60%</td>
        </tr>
    </table>
    """
    st.markdown(performance_html, unsafe_allow_html=True)
    with stylable_container(
        key="get_started_button",
        css_styles=button_style,
        ):
            st.button("Посмотреть ответы", key="review_btn")

    st.markdown("---")
    st.markdown("### Рекомендации")
    st.markdown("Основываясь на твоих успехах, мы рекомендуем следующие темы.")

    with st.container():
        st.markdown("""
        <div class="test-card">
            <h3>Основы структур данных</h3>
            <p>Протестируй свои знания в структурах данных</p>
            <p><strong>15 вопросов</strong> | <strong>30 минут</strong></p>
            <span class="topic-tag">Структуры данных</span>
            <div style="margin-top: 15px;">
                <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Начать тест</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="test-card">
            <h3>Анализ алгоритмов</h3>
            <p>Вопросы о сложностной оценки по времени и по памяти</p>
            <p><strong>10 вопросов</strong> | <strong>20 минут</strong></p>
            <span class="topic-tag">Алгоритмы</span>
            <span class="topic-tag">Сложностной анализ</span>
            <div style="margin-top: 15px;">
                <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Начать тест</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class="test-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3>Проблемы динамики</h3>
                    <p>Решай динамическое программирование</p>
                    <p><strong>7 вопросов</strong> | <strong>30 минут</strong></p>
                    <span class="topic-tag">Динамическое программирование</span>
                    <span class="topic-tag">Алгоритмы</span>
                </div>
                <div style="color: orange; font-weight: bold;">Давно не изучал эту тему!</div>
            </div>
            <div style="margin-top: 15px;">
                <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Начать тест</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

with summary_col:
    st.markdown("""
    <div class="test-card">
        <div class="summary-title">Результаты теста</div>
        <div class="summary-item">
            <div class="summary-label">Потраченное время</div>
            <div class="summary-value highlight-value">2 минуты</div>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
            <div class="summary-label">Сложность</div>
            <div class="summary-value">Средняя</div>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
            <div class="summary-label">Вопросы</div>
            <div class="summary-value highlight-value">5</div>
        </div>
        <div class="summary-divider"></div>
        <div class="summary-item">
            <div class="summary-label">Тема</div>
            <div class="summary-value">Структуры данных</div>
        </div>
    </div>
    """, unsafe_allow_html=True)