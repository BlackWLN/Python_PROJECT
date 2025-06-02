import streamlit as st
import time

# Data
questions = [
    {
        "question": "Какая структура данных использует принцип 'первый зашел - первый вышел'?",
        "type": "multiple_choice",
        "options": ["Очередь", "Стэк", "Связный список", "Дерево"],
        "correct_answer": "Cтэк",
    },
    {
        "question": "Какая временная сложность добавления элемента в массив?",
        "type": "multiple_choice",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "correct_answer": "O(1)",
    },
    {
        "question": "Как называется бинарное дерево, в котором каждый узел имеет или ноль или два ребенка?",
        "type": "multiple_choice",
        "options": ["Полное дерево", "Завершенное дерево", "Идеальное дерево", "Сбалансированное дерево"],
        "correct_answer": "Полное дерево",
    },
    {
        "question": "Объясни разницу между стэком и очередью.",
        "type": "text",
    },
    {
        "question": "Что подразумевается под временной сложностью?",
        "type": "text",
    },
    {
        "question": "Какая временная сложность поиска элемента в массиве?",
        "type": "multiple_choice",
        "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
        "correct_answer": "O(n)",
    },
]

if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = [""] * len(questions)
if "question_status" not in st.session_state:
    st.session_state.question_status = ["Нет ответа"] * len(questions)
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "timer_running" not in st.session_state:
    st.session_state.timer_running = True 
if "total_time" not in st.session_state:
    st.session_state.total_time = 30 * 60  # 30 minutes

def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes):02}:{int(seconds):02}"

def next_question():
    st.session_state.current_question = min(
        st.session_state.current_question + 1, len(questions) - 1
    )

def prev_question():
    st.session_state.current_question = max(
        st.session_state.current_question - 1, 0
    )

def submit_answer():
    question_index = st.session_state.current_question
    current_question_data = questions[question_index]

    if current_question_data["type"] == "multiple_choice":
        if st.session_state.selected_option:
            st.session_state.answers[question_index] = st.session_state.selected_option
            st.session_state.question_status[question_index] = "Ответ сохранён"
    elif current_question_data["type"] == "text":
        if st.session_state.text_answer:
            st.session_state.answers[question_index] = st.session_state.text_answer
            st.session_state.question_status[question_index] = "Ответ сохранён"

def navigate_to_question(question_number):
    st.session_state.current_question = question_number

def finish_test():
    st.session_state.timer_running = False
    st.write("Тест завершен!")

st.set_page_config(page_title="Основы структур данных", page_icon="💻", layout="centered")


st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div[data-testid="stHorizontalBlock"] > div:first-child > div > div > div > button {
            width: 40px;
            height: 40px;
            margin: 2px;
        }
    </style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 3])
with col1:
    st.markdown("[Выйти из теста](#)")

with col2:
    if st.session_state.timer_running:
        time_elapsed = int(time.time() - st.session_state.start_time)
        remaining_time = max(0, st.session_state.total_time - time_elapsed)
    else:
        time_elapsed = int(time.time() - st.session_state.start_time)
        remaining_time = max(0, st.session_state.total_time - time_elapsed)

    st.markdown(f"<p style='text-align: right;'>{format_time(remaining_time)}</p>", unsafe_allow_html=True)

st.title("Основы структур данных")

# Progress Bar
progress_value = (st.session_state.current_question + 1) / len(questions)
col1, col2 = st.columns([3, 1])

with col1:
    st.progress(progress_value)
with col2:
    unanswered_count = st.session_state.question_status.count("Нет ответа")
    st.markdown(f"Вопрос {st.session_state.current_question + 1} из {len(questions)}", unsafe_allow_html=True)

# Main
col1, col2, col3 = st.columns([1, 5, 2])

with col1:
    for i in range(len(questions)):
        status = st.session_state.question_status[i]
        button_label = f"{i+1}"
        button_type = "primary" if st.session_state.current_question == i else "secondary"
        if st.session_state.question_status[i] == "Ответ сохранён":
            button_type = "primary"

        st.button(
            button_label,
            key=f"nav_{i}",
            on_click=navigate_to_question,
            args=(i,),
            use_container_width=False,
            type=button_type
        )
    
with col2:
    st.subheader(f"Вопрос {st.session_state.current_question + 1} из {len(questions)}")

    question_data = questions[st.session_state.current_question]
    st.write(question_data["question"])

    if question_data["type"] == "multiple_choice":
        st.session_state.selected_option = st.radio(
            "", options=question_data["options"], key=f"radio_{st.session_state.current_question}"
        )
    elif question_data["type"] == "text":
        st.session_state.text_answer = st.text_area(
            "Пиши свой ответ здесь...",
            value=st.session_state.answers[st.session_state.current_question],
            height=150,
            key=f"text_area_{st.session_state.current_question}",
        )

    st.button("Сохранить ответ", on_click=submit_answer)
    
with col3:
    if st.button("Завершить", key="finish_button"):
        st.success("Тест завершён!")