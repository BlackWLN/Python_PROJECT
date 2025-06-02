import streamlit as st
from streamlit.components.v1 import html


st.set_page_config(page_title="Зарегистрироваться", page_icon="💻", layout="wide")

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("button_style.css") as b:
    button_style = b.read()

# Main
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown(
        """
        <div style="text-align: left; margin-bottom: 20px;">
            <button onclick="window.history.back()" class="back-button">← Вернуться домой</button>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<h1 style='text-align: center;'>Добро пожаловать!</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666; margin-bottom: 30px;'>Зарегистрируйтесь, чтобы следить за своими результатами</p>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        name = st.text_input("Имя", placeholder="Введите имя")
        email = st.text_input("Почта", placeholder="Введите почту")
        password = st.text_input("Пароль", type="password", placeholder="Введите пароль")
        sign_in = st.form_submit_button("Зарегистрироваться", use_container_width=True)
        
        if sign_in:
            if email and password and name:
                st.success("Успешно!")
            if not name:
                st.error("Введите имя")
            if not email:
                st.error("Введите почту")
            if not password:
                st.error("Введите пароль")
    
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
    
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
        <a href="#" style="color: #4a8bfc; text-decoration: none;">Войти</a>
        </div>
        """,
        unsafe_allow_html=True
    )