import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container


with open("button_style.css") as b:
    button_style = b.read()

# Page configuration
st.set_page_config(
    page_title="Тренажер для подготовки к ФИ и АиСД",
    page_icon="💻",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            background-color: #f8f9fa;
        }
        .centered-wrapper {
            display: flex;
            justify-content: center;
            width: 100%;
        }
        
        .centered-content {
            max-width: 800px;
            width: 100%;
            text-align: center;
        }
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            height: 100%;
            color: black;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            color: #4a6bdf;
        }
        .stats-card {
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            color: black;
        }
        .stats-number {
            font-size: 2rem;
            font-weight: bold;
            color: #4a6bdf;
            margin-bottom: 5px;
        }
        .stats-label {
            font-size: 1rem;
            color: #6c757d;
        }
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


# Header
with st.container():
    st.markdown('<div class="centered-wrapper"><div class="centered-content">', unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Тренажер для подготовки к ФИ и АиСД</h1>", unsafe_allow_html=True)
    with stylable_container(
        key="get_started_button",
        css_styles=button_style,
    ):
        st.markdown('<div class="centered-wrapper"><div class="centered-content">', unsafe_allow_html=True)
        st.button("Начать!")
        st.markdown('</div></div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #363636;'>Изучайте основы фундаментальной информатики и алгоритмы с помощью нашей платформы для подготовки к зачетам. Практикуйтесь на реальных экзаменационных вопросах и повышайте свою уверенность. </h4>", unsafe_allow_html=True)
    
st.markdown('<div class="centered-wrapper"></div>', unsafe_allow_html=True)

# Main
st.header("Наши возможности", divider="blue")

features = st.columns(3)

with features[0]:
    with st.container():
        st.markdown('<div class="feature-card">'
                    '<h3>Подробные темы</h3>'
                    '<p>Подробные вопросы, структуры данных, '
                    'и многое другое с объяснениями</p>'
                    '</div>', unsafe_allow_html=True)

with features[1]:
    with st.container():
        st.markdown('<div class="feature-card">'
                    '<h3>Адаптивное обучение</h3>'
                    '<p>Наши персональные рекомендации, основанные на ваших показателях</p>'
                    '</div>', unsafe_allow_html=True)

with features[2]:
    with st.container():
        st.markdown('<div class="feature-card">'
                    '<h3>Комьюнити</h3>'
                    '<p>Составление вопросов обучающимися для других '
                    'учащихся в благоприятной среде</p>'
                    '</div>', unsafe_allow_html=True)

st.header("Наш вклад", divider="blue")

stats = st.columns(3)

with stats[0]:
    with st.container():
        st.markdown('<div class="stats-card">'
                    '<div class="stats-number">10+</div>'
                    '<div class="stats-label">Активных студентов</div>'
                    '</div>', unsafe_allow_html=True)

with stats[1]:
    with st.container():
        st.markdown('<div class="stats-card">'
                    '<div class="stats-number">30+</div>'
                    '<div class="stats-label">Практических вопросов</div>'
                    '</div>', unsafe_allow_html=True)

with stats[2]:
    with st.container():
        st.markdown('<div class="stats-card">'
                    '<div class="stats-number">+10%</div>'
                    '<div class="stats-label">Процент успеха</div>'
                    '</div>', unsafe_allow_html=True)


st.markdown('<div class="centered-wrapper"><div class="centered-content">', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Готовы сдать зачеты на отлично?</h1>", unsafe_allow_html=True)
with stylable_container(key="get_started_button_2", css_styles=button_style):
    st.markdown('<div class="centered-wrapper"><div class="centered-content">', unsafe_allow_html=True)
    st.button("ДА!")
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
# Footer
st.markdown("---")
st.markdown("© 2025 Black_WLN & sswerty & annplv & mariakotik456")