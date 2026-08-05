import streamlit as st

import api_client
from auth_utils import log_in, is_authenticated, is_valid_email
from styles import read_css, hide_streamlit_chrome

st.set_page_config(page_title="Войти", page_icon="💻", layout="wide")
hide_streamlit_chrome()

# Custom CSS to style the page
st.markdown(f"<style>{read_css('style.css')}</style>", unsafe_allow_html=True)
button_style = read_css("button_style.css")

if is_authenticated():
    st.success("Вы уже вошли в аккаунт.")
    st.page_link("home_page.py", label="На главную", icon="🏠")
    st.stop()

# Main content
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

    # Welcome header
    st.markdown("<h1 style='text-align: center;'>Добро пожаловать!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Войдите чтобы следить за своими результатами</p>", unsafe_allow_html=True)

    # Login form
    with st.form("login_form"):
        email = st.text_input("Почта", placeholder="Введите почту")
        password = st.text_input("Пароль", type="password", placeholder="Введите пароль")

        sign_in = st.form_submit_button("Войти", use_container_width=True)

        if sign_in:
            if not email:
                st.error("Введите почту")
            elif not is_valid_email(email):
                st.error("Введите корректный email, например name@example.com")
            elif not password:
                st.error("Введите пароль")
            else:
                try:
                    log_in(email, password)
                    st.success("Успешно! Переходим...")
                    st.switch_page("home_page.py")
                except api_client.ApiError as exc:
                    if exc.status_code == 401:
                        st.error("Неверная почта или пароль")
                    else:
                        st.error(f"Не удалось войти: {exc}")

    # OR divider
    st.markdown(
        """
        <div style="display: flex; align-items: center; margin: 20px 0;">
            <div style="flex-grow: 1; height: 1px; background-color: #ddd;"></div>
            <div style="padding: 0 10px; color: #888;">ИЛИ ЗАРЕГИСТРИРОВАТЬСЯ</div>
            <div style="flex-grow: 1; height: 1px; background-color: #ddd;"></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Sign up link - центрируем в блоке
    link_col1, link_col2, link_col3 = st.columns([1, 2, 1])
    with link_col2:
        st.page_link("pages/2_page_sign_up.py", label="Нет аккаунта? Регистрация", icon="✍️")
