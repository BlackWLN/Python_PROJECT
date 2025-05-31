import streamlit as st
from streamlit.components.v1 import html


st.set_page_config(page_title="Войти", page_icon="💻", layout="wide")

# Custom CSS to style the page
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("button_style.css") as b:
    button_style = b.read()

# Main content
col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    # Back button (would need JavaScript to actually go back)
    st.markdown(
        """
        <div style="text-align: left; margin-bottom: 20px;">
            <button onclick="window.history.back()" class="back-button">← Вернуться домой</button>
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
        
        
        # Sign in button
        sign_in = st.form_submit_button("Войти", use_container_width=True)
        
        if sign_in:
            if email and password:
                st.success("Успешно!")
            if not email:
                st.error("Введите почту")
            if not password:
                st.error("Введите пароль")
    
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
    
    # Sign up link
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            Нет аккаунта? <a href="#" style="color: #4a8bfc; text-decoration: none;">Регистрация</a>
        </div>
        """,
        unsafe_allow_html=True
    )