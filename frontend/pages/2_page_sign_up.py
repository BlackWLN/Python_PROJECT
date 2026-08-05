import streamlit as st

import api_client
from auth_utils import log_in, is_authenticated, is_valid_email
from styles import read_css, hide_streamlit_chrome

st.set_page_config(page_title="Зарегистрироваться", page_icon="💻", layout="wide")
hide_streamlit_chrome()

st.markdown(f"<style>{read_css('style.css')}</style>", unsafe_allow_html=True)
button_style = read_css("button_style.css")

if is_authenticated():
    st.success("Вы уже вошли в аккаунт.")
    st.page_link("home_page.py", label="На главную", icon="🏠")
    st.stop()

# Main
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown(
        """
        <div style="text-align: left; margin-bottom: 20px;">
            <button onclick="window.history.back()" class="back-button">← Вернуться</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h1 style='text-align: center;'>Добро пожаловать!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Зарегистрируйтесь, чтобы следить за своими результатами</p>", unsafe_allow_html=True)

    with st.form("signup_form"):
        name = st.text_input("Имя", placeholder="Введите имя")
        email = st.text_input("Почта", placeholder="Введите почту")
        password = st.text_input("Пароль", type="password", placeholder="Введите пароль")
        sign_up = st.form_submit_button("Зарегистрироваться", use_container_width=True)

        if sign_up:
            if not name:
                st.error("Введите имя")
            elif not email:
                st.error("Введите почту")
            elif not is_valid_email(email):
                st.error("Введите корректный email, например name@example.com")
            elif not password:
                st.error("Введите пароль")
            elif len(password) < 6:
                st.error("Пароль должен быть не короче 6 символов")
            else:
                try:
                    api_client.register(name, email, password)
                    log_in(email, password)
                    st.success("Успешно! Переходим...")
                    st.switch_page("home_page.py")
                except api_client.ApiError as exc:
                    if exc.status_code == 400:
                        st.error("Этот email уже зарегистрирован")
                    else:
                        st.error(f"Не удалось зарегистрироваться: {exc}")

    st.markdown(
        """
        <div style="display: flex; align-items: center; margin: 20px 0;">
            <div style="flex-grow: 1; height: 1px; background-color: #ddd;"></div>
            <div style="padding: 0 10px; color: #888;">Уже есть аккаунт?</div>
            <div style="flex-grow: 1; height: 1px; background-color: #ddd;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.page_link("pages/1_page_sign_in.py", label="Войти", icon="🔑")
