import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="Выбрать тест", page_icon="💻", layout="wide")

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

st.header("Доступные тесты")
st.subheader("Выбери из имеющихся тестов или создай свой")

# Filters
with st.expander("Фильтр тестов"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.selectbox("Сложность", ["Все сложности", "Легкий", "Средний", "Сложный"], key="difficulty")
    
    with col2:
        st.selectbox("Время", ["Любая длительность", "< 15 мин", "15-30 мин", "> 30 мин"], key="time_limit")
    
    with col3:
        selected_topics = st.multiselect(
            "Темы",
            ["Алгоритмы", "Структуры данных", "Анализ сложности", 
             "Динамическое программирование", "Сортировка", "Поиск"],
            default=[],
            placeholder="Выбери тему"
        )
        

st.button("Сделать свой тест", type="primary")

# Recommended section
st.header("Рекомендовано")
st.write("Основано на твоих прошлых результатах тестов")

# Recommended test card
with st.container():
    st.markdown("""
    <div class="test-card">
        <h3>Непростые алгоритмы</h3>
        <p>Попытайся одолеть их!</p>
        <p><strong>8 вопросов</strong> | <strong>25 минут</strong> | <strong>4.9/5.0</strong></p>
        <span class="topic-tag">Алгоритмы</span>
        <div style="margin-top: 15px;">
            <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Начать тест</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Available tests section
st.header("Доступные тесты")

# Test 1
with st.container():
    st.markdown("""
    <div class="test-card">
        <h3>Основы структур данных</h3>
        <p>Протестируй свои знания в структурах данных</p>
        <p><strong>15 вопросов</strong> | <strong>30 минут</strong> | <strong>4.7/5.0</strong></p>
        <span class="topic-tag">Структуры данных</span>
        <div style="margin-top: 15px;">
            <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Начать тест</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Test 2
with st.container():
    st.markdown("""
    <div class="test-card">
        <h3>Анализ алгоритмов</h3>
        <p>Вопросы о сложностной оценки по времени и по памяти</p>
        <p><strong>10 вопросов</strong> | <strong>20 минут</strong> | <strong>4.2/5.0</strong></p>
        <span class="topic-tag">Алгоритмы</span>
        <span class="topic-tag">Сложностной анализ</span>
        <div style="margin-top: 15px;">
            <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">Начать тест</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Test 3 with warning
with st.container():
    st.markdown("""
    <div class="test-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h3>Проблемы динамики</h3>
                <p>Решай динамическое программирование</p>
                <p><strong>7 вопросов</strong> | <strong>30 минут</strong> | <strong>4.8/5.0</strong></p>
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
