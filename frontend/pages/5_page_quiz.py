import random
import time
from collections import defaultdict

import streamlit as st
from streamlit_extras.stylable_container import stylable_container

import api_client
from auth_utils import require_login, render_logout_sidebar
from styles import hide_streamlit_chrome

st.set_page_config(page_title="Прохождение теста", page_icon="💻", layout="wide")
hide_streamlit_chrome()

require_login()

if "quiz_config" not in st.session_state:
    st.warning("Сначала выбери тест.")
    st.page_link("pages/4_page_select_test.py", label="Выбрать тест", icon="📝")
    render_logout_sidebar()
    st.stop()


def format_time(seconds: int) -> str:
    minutes, seconds = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02}:{seconds:02}"


@st.cache_data(show_spinner=False, ttl=300)
def _fetch_answers(question_id: int):
    return api_client.get_answers(question_id)


def build_quiz():
    config = st.session_state["quiz_config"]
    pool = []
    for theme in config["themes"]:
        try:
            pool.extend(api_client.get_questions(subject=config["subject"], theme=theme))
        except api_client.ApiError as exc:
            st.error(f"Не удалось загрузить вопросы по теме «{theme}»: {exc}")

    random.shuffle(pool)
    pool = pool[: config.get("question_count") or len(pool)]

    quiz_questions = []
    for q in pool:
        try:
            answers = _fetch_answers(q["question_id"])
        except api_client.ApiError:
            continue
        if not answers:
            continue
        shuffled = answers[:]
        random.shuffle(shuffled)
        quiz_questions.append({
            "question_id": q["question_id"],
            "question_text": q["question_text"],
            "theme": q["theme"],
            "answers": shuffled,  # каждый answer: {answer_id, answer_text, is_correct, question_id}
        })

    st.session_state["quiz_questions"] = quiz_questions
    st.session_state["current_question"] = 0
    st.session_state["selected_answers"] = [None] * len(quiz_questions)
    st.session_state["question_status"] = ["Нет ответа"] * len(quiz_questions)
    st.session_state["submitted_flags"] = [False] * len(quiz_questions)
    st.session_state["start_time"] = time.time()
    st.session_state["question_first_seen"] = [None] * len(quiz_questions)
    st.session_state["question_time_spent"] = [0] * len(quiz_questions)


if "quiz_questions" not in st.session_state:
    with st.spinner("Загружаем вопросы..."):
        build_quiz()

questions = st.session_state["quiz_questions"]

if not questions:
    st.warning("По выбранным темам не нашлось вопросов с ответами.")
    st.page_link("pages/4_page_select_test.py", label="Выбрать другой тест", icon="📝")
    render_logout_sidebar()
    st.stop()

config = st.session_state["quiz_config"]
time_limit = config.get("time_limit")

if st.button("← Главная", key="home_button"):
    st.switch_page("home_page.py")

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("Прервать тест"):
        for key in ("quiz_config", "quiz_questions", "current_question", "selected_answers",
                    "question_status", "submitted_flags", "start_time", "question_first_seen",
                    "question_time_spent"):
            st.session_state.pop(key, None)
        st.switch_page("pages/4_page_select_test.py")

with col2:
    elapsed = int(time.time() - st.session_state["start_time"])
    if time_limit:
        remaining = max(0, time_limit - elapsed)
        st.markdown(f"<p style='text-align: right;'>Осталось: {format_time(remaining)}</p>", unsafe_allow_html=True)
        time_is_up = remaining <= 0
    else:
        st.markdown(f"<p style='text-align: right;'>Прошло: {format_time(elapsed)}</p>", unsafe_allow_html=True)
        time_is_up = False

st.title(f"{config['subject']}: тест по выбранным темам")

current = st.session_state["current_question"]

# отмечаем момент первого показа вопроса, чтобы посчитать время ответа
if st.session_state["question_first_seen"][current] is None:
    st.session_state["question_first_seen"][current] = time.time()

progress_value = (current + 1) / len(questions)
st.caption(f"Вопрос {current + 1} из {len(questions)}")
st.progress(progress_value)


def navigate_to(idx: int):
    st.session_state["current_question"] = idx


def save_current_answer():
    idx = st.session_state["current_question"]
    selected_id = st.session_state.get(f"radio_{idx}")
    if selected_id is not None:
        st.session_state["selected_answers"][idx] = selected_id
        st.session_state["question_status"][idx] = "Ответ сохранён"
        first_seen = st.session_state["question_first_seen"][idx]
        if first_seen:
            st.session_state["question_time_spent"][idx] = int(time.time() - first_seen)


def submit_all_answers():
    """Отправляет на бэкенд все отвеченные, но ещё не отправленные вопросы."""
    for idx, q in enumerate(questions):
        selected_id = st.session_state["selected_answers"][idx]
        if selected_id is None or st.session_state["submitted_flags"][idx]:
            continue
        try:
            api_client.submit_answer(
                question_id=q["question_id"],
                selected_answer_id=selected_id,
                time_spent=st.session_state["question_time_spent"][idx] or None,
            )
            st.session_state["submitted_flags"][idx] = True
        except api_client.ApiError as exc:
            st.error(f"Не удалось сохранить ответ на вопрос {idx + 1}: {exc}")


# Навигация по вопросам - сеткой по 5 в ряд, а не одной длинной колонкой
# (иначе список из 10+ кнопок растягивается на весь экран по вертикали).
# Кнопки специально маленькие (через stylable_container), чтобы не отвлекали
# от самого вопроса.
_nav_button_css = """
button {
    padding: 0.1rem 0 !important;
    min-height: 1.8rem !important;
    height: 1.8rem !important;
    font-size: 0.8rem !important;
}
"""
NAV_PER_ROW = 5
with stylable_container(key="quiz_nav_grid", css_styles=_nav_button_css):
    for row_start in range(0, len(questions), NAV_PER_ROW):
        row_indices = range(row_start, min(row_start + NAV_PER_ROW, len(questions)))
        nav_row_cols = st.columns(NAV_PER_ROW)
        for col, i in zip(nav_row_cols, row_indices):
            with col:
                status = st.session_state["question_status"][i]
                button_type = "primary" if (current == i or status == "Ответ сохранён") else "secondary"
                st.button(str(i + 1), key=f"nav_{i}", on_click=navigate_to, args=(i,),
                          type=button_type, use_container_width=True)

st.divider()

col_main, col_finish = st.columns([4, 1])

with col_main:
    question_data = questions[current]
    st.subheader(f"Вопрос {current + 1} из {len(questions)}")
    st.caption(f"Тема: {question_data['theme']}")
    st.write(question_data["question_text"])

    options = {a["answer_text"]: a["answer_id"] for a in question_data["answers"]}
    previously_selected_id = st.session_state["selected_answers"][current]
    previously_selected_text = next(
        (text for text, aid in options.items() if aid == previously_selected_id), None
    )
    default_index = list(options.keys()).index(previously_selected_text) if previously_selected_text else None

    chosen_text = st.radio(
        "Выбери ответ:",
        options=list(options.keys()),
        index=default_index,
        key=f"radio_text_{current}",
    )
    st.session_state[f"radio_{current}"] = options.get(chosen_text)

    nav_cols = st.columns(3)
    with nav_cols[0]:
        if st.button("Сохранить ответ", on_click=save_current_answer):
            pass
    with nav_cols[1]:
        if current > 0 and st.button("Назад"):
            navigate_to(current - 1)
            st.rerun()
    with nav_cols[2]:
        if current < len(questions) - 1 and st.button("Далее"):
            save_current_answer()
            navigate_to(current + 1)
            st.rerun()

def finish_test():
    save_current_answer()
    with st.spinner("Сохраняем результаты..."):
        submit_all_answers()

    by_theme = defaultdict(lambda: {"total": 0, "correct": 0})
    total_correct = 0
    total_answered = 0
    for i, q in enumerate(questions):
        selected_id = st.session_state["selected_answers"][i]
        if selected_id is None:
            continue
        total_answered += 1
        is_correct = any(a["answer_id"] == selected_id and a["is_correct"] for a in q["answers"])
        by_theme[q["theme"]]["total"] += 1
        if is_correct:
            total_correct += 1
            by_theme[q["theme"]]["correct"] += 1

    st.session_state["last_result"] = {
        "subject": config["subject"],
        "total_questions": len(questions),
        "answered": total_answered,
        "correct": total_correct,
        "time_spent": int(time.time() - st.session_state["start_time"]),
        "by_theme": dict(by_theme),
    }
    st.switch_page("pages/6_page_quiz_final.py")


with col_finish:
    unanswered = st.session_state["question_status"].count("Нет ответа")
    st.metric("Осталось без ответа", unanswered)
    if st.button("Завершить тест", type="primary"):
        finish_test()

if time_is_up:
    st.warning("Время вышло! Завершаем тест...")
    finish_test()

render_logout_sidebar()
