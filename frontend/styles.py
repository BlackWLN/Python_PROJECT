"""Хелпер для чтения CSS-файлов вне зависимости от текущей рабочей директории.

Streamlit Cloud (и некоторые другие хостинги) запускают приложение с cwd =
корень репозитория, а не папка frontend/, поэтому bare-relative open("style.css")
не находит файл. Тут путь всегда считается от расположения этого модуля.
"""
from pathlib import Path

import streamlit as st

FRONTEND_DIR = Path(__file__).resolve().parent


def read_css(filename: str) -> str:
    return (FRONTEND_DIR / filename).read_text(encoding="utf-8")


def hide_streamlit_chrome() -> None:
    """Полностью убирает сайдбар (гамбургер-меню и кнопка Deploy убираются
    отдельно, через toolbarMode="minimal" в .streamlit/config.toml - это
    официально поддерживаемый способ, в отличие от CSS-хака ниже).

    В приложении нигде больше не используется st.sidebar (см. auth_utils.
    render_logout_sidebar - блок "вошли как/выйти" рендерится в самом контенте
    страницы), поэтому безопасно скрыть контейнер сайдбара целиком: он не
    просто прячет список страниц, а схлопывает саму колонку, чтобы контент
    занимал всю ширину, а не оставлял пустую полосу слева.
    Вызывать сразу после st.set_page_config() (сам set_page_config должен
    остаться первой командой на странице).
    """
    st.markdown("""
        <style>
        [data-testid="stSidebar"] { display: none !important; }
        </style>
    """, unsafe_allow_html=True)
