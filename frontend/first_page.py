import streamlit as st
from streamlit_extras.colored_header import colored_header
from streamlit_extras.stylable_container import stylable_container




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
            color: white !important;
            background-color: #3a5bcf;
        }
        .stButton>button:focus {
            border: 2px solid white;
            color: white !important;
        }
        
    </style>
""", unsafe_allow_html=True)

button_style = """
button {
  display: block; 
  margin: 0 auto;
  position: relative;
  padding: 10px 20px;
  border-radius: 7px;
  border: 1px solid rgb(61, 106, 255);
  font-size: 14px;
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 2px;
  background: transparent;
  color: #fff;
  overflow: hidden;
  box-shadow: 0 0 0 0 transparent;
  -webkit-transition: all 0.2s ease-in;
  -moz-transition: all 0.2s ease-in;
  transition: all 0.2s ease-in;
}

button:hover {
border-radius: 7px;
  border: 1px solid rgb(255, 255, 255);
  color: #fff;
  background: rgb(61, 106, 255);
  box-shadow: 0 0 30px 5px rgba(0, 142, 236, 0.815);
  -webkit-transition: all 0.2s ease-out;
  -moz-transition: all 0.2s ease-out;
  transition: all 0.2s ease-out;
}

button:hover::before {
  border: 1px solid rgb(255, 255, 255);
  color: #fff;
  -webkit-animation: sh02 0.5s 0s linear;
  -moz-animation: sh02 0.5s 0s linear;
  animation: sh02 0.5s 0s linear;
}

button::before {
  border: 1px solid rgb(255, 255, 255);
  color: #fff;
  content: '';
  display: block;
  width: 0px;
  height: 86%;
  position: absolute;
  top: 7%;
  left: 0%;
  opacity: 0;
  background: #fff;
  box-shadow: 0 0 50px 30px #fff;
  -webkit-transform: skewX(-20deg);
  -moz-transform: skewX(-20deg);
  -ms-transform: skewX(-20deg);
  -o-transform: skewX(-20deg);
  transform: skewX(-20deg);
}

@keyframes sh02 {
  from {
    opacity: 0;
    left: 0%;
  }

  50% {
    opacity: 1;
  }

  to {
    opacity: 0;
    left: 100%;
  }
}

button:active {
  border: 1px solid rgb(255, 255, 255);
  color: #fff;
  box-shadow: 0 0 0 0 transparent;
  -webkit-transition: box-shadow 0.2s ease-in;
  -moz-transition: box-shadow 0.2s ease-in;
  transition: box-shadow 0.2s ease-in;
}
        """

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
    st.markdown("<h4 style='text-align: center; color: #c7c7c7;'>Изучайте основы фундаментальной информатики и алгоритмы с помощью нашей платформы для подготовки к зачетам. Практикуйтесь на реальных экзаменационных вопросах и повышайте свою уверенность. </h4>", unsafe_allow_html=True)
    
st.markdown('<div class="centered-wrapper"></div>', unsafe_allow_html=True)


# Features Section
st.header("Наши возможности", divider="blue")

features = st.columns(3)

with features[0]:
    with st.container():
        st.markdown('<div class="feature-card">'
                    '<div class="feature-icon">📚</div>'
                    '<h3>Подробные темы</h3>'
                    '<p>Подробные вопросы, структуры данных, '
                    'и многое другое с объяснениями</p>'
                    '</div>', unsafe_allow_html=True)

with features[1]:
    with st.container():
        st.markdown('<div class="feature-card">'
                    '<div class="feature-icon">🔍</div>'
                    '<h3>Адаптивное обучение</h3>'
                    '<p>Наши персональные рекомендации, основанные на ваших '
                    'показателях и особенностях обучения</p>'
                    '</div>', unsafe_allow_html=True)

with features[2]:
    with st.container():
        st.markdown('<div class="feature-card">'
                    '<div class="feature-icon">👥</div>'
                    '<h3>Комьюнити</h3>'
                    '<p>Составление вопросов обучающимися для других '
                    'учащихся в благоприятной среде</p>'
                    '</div>', unsafe_allow_html=True)

# Stats Section
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
st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>Готовы сдать зачеты по ФИ и АиСД на отлично?</h1>", unsafe_allow_html=True)
with stylable_container(key="get_started_button_2", css_styles=button_style):
    st.markdown('<div class="centered-wrapper"><div class="centered-content">', unsafe_allow_html=True)
    st.button("ДА!")
    st.markdown('</div></div>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)
# Footer
st.markdown("---")
st.markdown("© 2025 Black_WLN & sswerty & annplv & mariakotik456")