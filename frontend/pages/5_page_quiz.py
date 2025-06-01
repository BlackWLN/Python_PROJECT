import streamlit as st

# Set page configuration
st.set_page_config(page_title="Основы структур данных", layout="wide")

# CSS styling
with open("quiz.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = 1
if 'answers' not in st.session_state:
    st.session_state.answers = {1: None, 2: None, 3: None, 4: None, 5: None}

# Question data
questions = {
    1: {
        "type": "mcq",
        "question": "Какая структура данных использует принцип первый зашел последний вышел?",
        "options": ["Очередь", "Стэк", "Связный список", "Дерево"],
        "correct_answer": 1  # index of correct option (0-based)
    },
    2: {
        "type": "mcq",
        "question": "Какая структура данных использует принцип первый зашел первый вышел?",
        "options": ["Массив", "Очередь", "Стэк", "Граф"],
        "correct_answer": 0
    },
    3: {
        "type": "mcq",
        "question": "У какой структуры данных сложность вставки элемента в начало O(1)?",
        "options": ["Массив", "Связный список", "Бинарное дерево", "Стэк"],
        "correct_answer": 1
    },
    4: {
        "type": "text",
        "question": "Объясни разницу между стэком и очередью."
    },
    5: {
        "type": "mcq",
        "question": "Какая структура данных обычно используется в рекурсии?",
        "options": ["Очередь", "Стэк", "Дерево", "Хэщ-таблица"],
        "correct_answer": 1
    }
}

# Navigation functions
def go_to_question(q_num):
    st.session_state.current_question = q_num

def next_question():
    if st.session_state.current_question < len(questions):
        st.session_state.current_question += 1

def prev_question():
    if st.session_state.current_question > 1:
        st.session_state.current_question -= 1

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main-container {
        display: flex;
        flex-direction: row;
        width: 100%;
    }
    .nav-column {
        width: 100%;
        padding: 10px;
        text-align: center; /* Center align text */
    }
    .question-column {
        width: 100%;
        padding: 10px;
        text-align: center; /* Center align text */
    }
    .finish-column {
        width: 100%;
        padding: 10px;
        text-align: center; /* Center align text */
    }
    .column-header {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .nav-buttons {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    .nav-buttons button {
        width: 100%;
    }
    .question {
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    .stRadio {
        width: 100%; /* Make radio buttons full width */
    }
    .stRadio > label {
        display: block;
        width: 100%;
        text-align: left;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-bottom: 5px;
    }

    .nav-controls {
        margin-top: 20px;
        display: flex;
        justify-content: space-between;
    }

    /* Center content within the columns */
    [data-testid="stColumn"] {
        display: flex;
        flex-direction: column;
        align-items: center; /* Horizontally center */
    }

    /* Optional: Ensure content takes up the full column height */
    [data-testid="stColumn"] > div {
        width: 100%;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

#Main app
st.title("Основы структур данных")

# Create columns for layout
nav_col, quest_col, finish_col = st.columns([1, 4, 1])

# Main container with navigation and question
with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    # Left navigation column - Questions
    with nav_col:
        st.markdown("""
        <div class="nav-column">
            <div class="column-header">Вопросы</div>
            <div class="nav-buttons">
        """, unsafe_allow_html=True)

        for q_num in range(1, 6):
            button_class = ""
            if q_num == st.session_state.current_question:
                button_class = "current"
            elif st.session_state.answers[q_num] is not None:
                button_class = "answered"
            else:
                button_class = "unanswered"

            if st.button(
                str(q_num),
                key=f"nav_{q_num}",
                on_click=go_to_question,
                args=(q_num,),
                type="secondary"
            ):
                pass

        st.markdown("""</div></div>""", unsafe_allow_html=True)

    # Middle question column
    with quest_col:
        st.markdown(f"""
        <div class="question-column">
            <div class="question-counter">Вопрос {st.session_state.current_question} из 5</div>
        """, unsafe_allow_html=True)

        # Display current question
        current_q = st.session_state.current_question
        q_data = questions[current_q]

        if q_data["type"] == "mcq":
            st.markdown(f'<div class="question">{q_data["question"]}</div>', unsafe_allow_html=True)

            # Display options
            selected = st.radio(
                "Выбери ответ:",
                q_data["options"],
                index=st.session_state.answers.get(current_q, None),
                key=f"q{current_q}_options",
                label_visibility="collapsed"
            )

            # Store answer
            if selected:
                st.session_state.answers[current_q] = q_data["options"].index(selected)

        elif q_data["type"] == "text":
            st.markdown(f'<div class="question">{q_data["question"]}</div>', unsafe_allow_html=True)

            # Text answer box
            answer = st.text_area(
                "Пиши ответ здесь...",
                value=st.session_state.answers.get(current_q, ""),
                key=f"q{current_q}_text",
                label_visibility="collapsed"
            )

            # Store answer
            if answer:
                st.session_state.answers[current_q] = answer

        # Navigation controls (Previous/Next)
        st.markdown('<div class="nav-controls">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.button("← Назад",
                     on_click=prev_question,
                     disabled=st.session_state.current_question == 1,
                     key="prev_btn",
                     help="Перейти к предыдущему вопросу")
        with col2:
            st.button("Вперед →",
                     on_click=next_question,
                     disabled=st.session_state.current_question == len(questions),
                     key="next_btn",
                     help="Перейти к следующему вопросу")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)  # Close question-column

    # Right finish column
    with finish_col:
        st.markdown("""
        <div class="finish-column">
            <div class="column-header">
        """, unsafe_allow_html=True)

        # Finish button
        if st.button("Закончить", key="finish_button"):
            st.success("Тест закончен успешно!")

        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)