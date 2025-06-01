import streamlit as st
from streamlit_extras.stylable_container import stylable_container

with open("button_style.css") as b:
    button_style = b.read()

st.set_page_config(page_title="Создать тест", page_icon="💻", layout="wide")

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

st.title("Создать новый тест")
st.subheader("Разработай свой кастомизированный тест с собственными вопросами и настройками")

with st.expander("## Детали", expanded=True):
    st.markdown("**Информация о тесте**  \nНастрой базовую информацию о твоем тесте")
    
    test_title = st.text_input("### Название теста", placeholder="Введи название, описывающее твой тест")
    test_description = st.text_area("### Описание (опционально)", placeholder="Опиши, какие знания может проверить твой тест")
    
    col1, col2 = st.columns(2)
    with col1:
        difficulty = st.selectbox("### Уровень сложности", ["Легкий", "Средний", "Сложный"], index=1)
    with col2:
        time_limit = st.number_input("Лимит времени (в минутах)", min_value=1, value=30)
    
    topics = st.multiselect(
        "### Темы",
        ["Алгоритмы", "Анализ сложности", "Динамическое программирование", "Поиск", "Структуры данных"],
        default=["Алгоритмы", "Анализ сложности"]
    )

st.divider()

st.subheader("Вопросы")
st.markdown("**Добавить вопросы**  \nСделай новые вопросы для твоего теста")

with st.form("question_form"):
    col1, col2 = st.columns(2)
    with col1:
        question_topic = st.selectbox("### Тема", topics if topics else ["Алгоритмы"])
    with col2:
        question_type = st.selectbox("### Тип вопроса", ["Множественный выбор", "Правда или ложь", "С коротким ответом"], index=0)
    
    question_text = st.text_area("### Вопрос", placeholder="Вводи свой вопрос здесь")
    
    if question_type == "Множественный выбор":
        st.markdown("### Варианты ответа")
        options = []
        for i in range(4):
            option = st.text_input(f"Вариант {i+1}", key=f"option_{i}", placeholder=f"Вариант {i+1}")
            options.append(option)
        correct_answer = st.radio("Выбери правильный ответ", [f"Вариант {i+1}" for i in range(4)], index=0)
    
    explanation = st.text_area("### Объяснение(опционально)", placeholder="Объясни правильный ответ")
    question_difficulty = st.select_slider("### Сложность", ["Легкий", "Средний", "Сложный"], value="Средний")
    
    submitted = st.form_submit_button("Сохранить вопрос")
    if submitted:
        st.success("Успешно!")


with stylable_container(
        key="get_started_button",
        css_styles=button_style,
    ):
        st.markdown('<div class="centered-wrapper"><div class="centered-content">', unsafe_allow_html=True)
        if st.button("Создать тест"):
            if not test_title:
                st.error("Пожалуйста, напишите название теста")
            else:
                st.success(f"Тест '{test_title}' создан успешно!")
        st.markdown('</div></div>', unsafe_allow_html=True)
