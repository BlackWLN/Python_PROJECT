"""Общие хелперы для работы с сессией пользователя в Streamlit-фронтенде."""
import re

import streamlit as st

import api_client

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    return bool(_EMAIL_RE.match(email.strip()))

# Streamlit сбрасывает st.session_state целиком при полном обновлении страницы
# в браузере (F5) - это новая сессия с его точки зрения. Чтобы логин переживал
# обновление, дублируем токен в query-параметр URL (?t=...) и восстанавливаем
# из него сессию, если session_state уже пуст.
#
# Компромисс: токен становится виден в адресной строке и в истории браузера -
# если кто-то скопирует такую ссылку, то сможет зайти под этим же аккаунтом.
# Для учебного портфолио-проекта это приемлемо; для продакшена лучше заменить
# на httpOnly-cookie через отдельный компонент (например streamlit-cookies-manager).
_TOKEN_PARAM = "t"


def _set_token_param(token: str) -> None:
    st.query_params[_TOKEN_PARAM] = token


def _clear_token_param() -> None:
    if _TOKEN_PARAM in st.query_params:
        del st.query_params[_TOKEN_PARAM]


def _restore_from_query_params() -> None:
    if st.session_state.get("access_token"):
        return
    token = st.query_params.get(_TOKEN_PARAM)
    if not token:
        return
    st.session_state["access_token"] = token
    try:
        me = api_client.get_me()
        st.session_state["user"] = {
            "email": me["email"],
            "account_id": me["account_id"],
            "account_name": me["account_name"],
        }
    except api_client.ApiError:
        # токен невалиден или истёк - подчищаем и сессию, и URL
        st.session_state.pop("access_token", None)
        _clear_token_param()


def is_authenticated() -> bool:
    _restore_from_query_params()
    return bool(st.session_state.get("access_token"))


def current_user() -> dict:
    return st.session_state.get("user", {})


def log_in(email: str, password: str) -> None:
    """Логинится через API, кладёт токен в сессию и в URL. Кидает api_client.ApiError при ошибке."""
    token_data = api_client.login(email, password)
    st.session_state["access_token"] = token_data["access_token"]
    me = api_client.get_me()
    st.session_state["user"] = {
        "email": me["email"],
        "account_id": me["account_id"],
        "account_name": me["account_name"],
    }
    _set_token_param(token_data["access_token"])


def log_out() -> None:
    for key in ("access_token", "user", "quiz_state"):
        st.session_state.pop(key, None)
    _clear_token_param()


def require_login() -> None:
    """Вызывать в начале страниц, которым нужен залогиненный пользователь.
    Если пользователь не залогинен - показывает сообщение и останавливает рендер страницы.
    """
    if not is_authenticated():
        st.warning("Сначала войдите в аккаунт, чтобы получить доступ к этой странице.")
        st.page_link("pages/1_page_sign_in.py", label="Перейти на страницу входа", icon="🔑")
        st.stop()


def render_logout_sidebar() -> None:
    """Небольшая строка "вошли как ... / Выйти" внизу контента страницы (не в st.sidebar!).

    st.sidebar сознательно не используется: сам контейнер сайдбара в Streamlit
    занимает место в вёрстке, даже если внутри него ничего нет или его список
    страниц спрятан через CSS - получается пустая колонка слева. Раз сайдбар
    в приложении больше нигде не нужен, проще вообще не рендерить в него.

    Специально маленькая и ненавязчивая, чтобы не отвлекать от контента
    страницы - вызывать в самом конце скрипта страницы, после всего остального.
    """
    if is_authenticated():
        st.divider()
        left, right = st.columns([6, 1])
        with left:
            st.caption(f"Вошли как {current_user().get('email', '')}")
        with right:
            if st.button("Выйти", key="logout_button"):
                log_out()
                st.rerun()
