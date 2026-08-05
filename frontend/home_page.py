import streamlit as st
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.stylable_container import stylable_container

import api_client
from auth_utils import is_authenticated, current_user, log_out
from styles import read_css, hide_streamlit_chrome

st.set_page_config(page_title="Главная", page_icon="💻", layout="wide")
hide_streamlit_chrome()

button_style = read_css("button_style_ease.css")

if not is_authenticated():
    # Анонимного посетителя сразу отправляем на публичный лендинг вместо стены логина
    st.switch_page("pages/3_page_greeting.py")

st.markdown("""
<style>
    .test-item { padding: 0.5rem 0; border-bottom: 1px solid #eee; }
    .achievement-card { border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin-bottom: 10px; background-color: #f9f9f9; }
    .topic-tag { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 0.8em; margin-right: 5px; margin-bottom: 5px; }
    .topic-tag.weak { background-color: #fdecea; color: #c0392b; }
    .topic-tag.strong { background-color: #eafaf1; color: #27ae60; }
    .stButton>button { border: 2px solid white; color: white; background-color: #4a6bdf; transition: all 0.3s ease; }
    .stButton>button:hover { border: 2px solid white; color: white; background-color: #3a5bcf; }
    .stButton>button:focus { border: 2px solid white; color: white; }
</style>
""", unsafe_allow_html=True)

header_left, header_right = st.columns([2, 3], vertical_alignment="center")
with header_left:
    st.subheader("Добро пожаловать!")
with header_right:
    action_cols = st.columns(3)
    with action_cols[0]:
        if st.button("Начать тест", use_container_width=True, type="primary", key="start_test_top"):
            st.switch_page("pages/4_page_select_test.py")
    with action_cols[1]:
        if st.button("Добавить вопрос", use_container_width=True, key="add_question_top"):
            st.switch_page("pages/7_page_create_test.py")
    with action_cols[2]:
        if st.button("Выйти", use_container_width=True, key="logout_top"):
            log_out()
            st.rerun()
    st.caption(f"Вошли как **{current_user().get('email', '')}**")

st.divider()

try:
    stats = api_client.get_statistics()
except api_client.ApiError as exc:
    st.error(f"Не удалось загрузить статистику: {exc}")
    stats = None

if not stats or stats.get("total_tests", 0) == 0:
    st.info("Ты ещё не прошёл ни одного теста. Начни прямо сейчас!")
    with stylable_container(key="start_first_test", css_styles=button_style):
        if st.button("Пройти первый тест", type="primary"):
            st.switch_page("pages/4_page_select_test.py")
    st.stop()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Тестов пройдено", value=stats["total_tests"])
with col2:
    st.metric(label="Средний результат", value=f"{round(stats['average_score'] * 100)}%")
with col3:
    minutes = stats["time_spent"] // 60
    st.metric(label="Время в тренажере", value=f"{minutes} мин")

style_metric_cards()

col_left, col_right = st.columns([2, 1])

with col_left:
    st.header("Недавние результаты")
    st.caption("Твои последние ответы")

    recent_html = ""
    for item in stats.get("recent_results", [])[:5]:
        mark = "✅" if item["result"] else "❌"
        date_str = item["date"].split("T")[0] if isinstance(item["date"], str) else str(item["date"])
        recent_html += f"""
        <div class="test-item">
            {mark} <strong>{item['theme']}</strong><br>
            <span style="color: #666;">{date_str}</span>
        </div>
        """
    st.markdown(recent_html or "<p>Пока нет данных</p>", unsafe_allow_html=True)

with col_right:
    st.header("Твой прогресс")
    st.caption(f"Место в общем рейтинге: {stats['rank']} из {stats['total_users']}")

    try:
        leaderboard = api_client.get_leaderboard(limit=10)
    except api_client.ApiError:
        leaderboard = []

    if leaderboard:
        my_id = current_user().get("account_id")
        for place, entry in enumerate(leaderboard, start=1):
            line = f"{place}. {entry['account_name']} — {round(entry['average_score'] * 100)}%"
            if entry["account_id"] == my_id:
                st.markdown(f"**{line} (ты)**")
            else:
                st.caption(line)

    if stats.get("weak_themes"):
        st.markdown("**Стоит подтянуть:**")
        st.markdown(
            "".join(f'<span class="topic-tag weak">{t}</span>' for t in stats["weak_themes"]),
            unsafe_allow_html=True
        )
    if stats.get("strong_themes"):
        st.markdown("**Сильные темы:**")
        st.markdown(
            "".join(f'<span class="topic-tag strong">{t}</span>' for t in stats["strong_themes"]),
            unsafe_allow_html=True
        )
    if not stats.get("weak_themes") and not stats.get("strong_themes"):
        st.write("Пройди ещё несколько тестов, чтобы увидеть разбивку по темам.")

st.divider()
bottom_cols = st.columns(2)
with bottom_cols[0]:
    if st.button("Начать тест", use_container_width=True, type="primary", key="start_test_bottom"):
        st.switch_page("pages/4_page_select_test.py")
with bottom_cols[1]:
    if st.button("Добавить вопрос", use_container_width=True, key="add_question_bottom"):
        st.switch_page("pages/7_page_create_test.py")
