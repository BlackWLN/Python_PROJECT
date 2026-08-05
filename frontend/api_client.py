"""Тонкий клиент для похода в FastAPI-бэкенд из Streamlit-фронтенда.

Адрес бэкенда берётся из (по приоритету):
1. st.secrets["API_BASE_URL"]        - для Streamlit Community Cloud
2. переменной окружения API_BASE_URL - для локального запуска / docker
3. http://localhost:8000             - дефолт для локальной разработки
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
import streamlit as st


class ApiError(Exception):
    """Ошибка запроса к API с человекочитаемым сообщением для показа в UI."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code


def _secrets_file_exists() -> bool:
    """Streamlit печатает красный варнинг прямо в приложение при любом
    обращении к st.secrets, если файла secrets.toml нет вообще (например на
    Railway, где всё идёт через переменные окружения) - даже если мы сами
    ловим исключение. Поэтому сначала проверяем на диске, стоит ли туда лезть."""
    candidates = [
        Path(__file__).resolve().parent / ".streamlit" / "secrets.toml",
        Path.home() / ".streamlit" / "secrets.toml",
    ]
    return any(p.exists() for p in candidates)


def get_base_url() -> str:
    if _secrets_file_exists():
        try:
            if "API_BASE_URL" in st.secrets:
                return st.secrets["API_BASE_URL"].rstrip("/")
        except Exception:
            pass
    return os.environ.get("API_BASE_URL", "http://localhost:8000").rstrip("/")


def _url(path: str) -> str:
    return f"{get_base_url()}/api/v1{path}"


def _handle_response(resp: requests.Response) -> Any:
    if resp.status_code >= 400:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        raise ApiError(str(detail), status_code=resp.status_code)
    if resp.status_code == 204 or not resp.content:
        return None
    return resp.json()


def _auth_headers() -> Dict[str, str]:
    token = st.session_state.get("access_token")
    if not token:
        raise ApiError("Вы не авторизованы", status_code=401)
    return {"Authorization": f"Bearer {token}"}


def register(name: str, email: str, password: str) -> Dict[str, Any]:
    try:
        resp = requests.post(
            _url("/auth/register"),
            json={"account_name": name, "email": email, "password": password},
            timeout=10,
        )
    except requests.RequestException as exc:
        raise ApiError(f"Не удалось связаться с сервером: {exc}")
    return _handle_response(resp)


def login(email: str, password: str) -> Dict[str, Any]:
    try:
        resp = requests.post(
            _url("/auth/login"),
            data={"username": email, "password": password},
            timeout=10,
        )
    except requests.RequestException as exc:
        raise ApiError(f"Не удалось связаться с сервером: {exc}")
    return _handle_response(resp)


def get_me() -> Dict[str, Any]:
    resp = requests.get(_url("/auth/me"), headers=_auth_headers(), timeout=10)
    return _handle_response(resp)


def get_leaderboard(limit: int = 20) -> List[Dict[str, Any]]:
    resp = requests.get(_url("/quiz/leaderboard"), headers=_auth_headers(), params={"limit": limit}, timeout=10)
    return _handle_response(resp)


def get_subjects() -> List[Dict[str, Any]]:
    resp = requests.get(_url("/quiz/subjects"), headers=_auth_headers(), timeout=10)
    return _handle_response(resp)


def get_questions(subject: Optional[str] = None, theme: Optional[str] = None) -> List[Dict[str, Any]]:
    params = {k: v for k, v in {"subject": subject, "theme": theme}.items() if v}
    resp = requests.get(_url("/quiz/questions"), headers=_auth_headers(), params=params, timeout=10)
    return _handle_response(resp)


def get_answers(question_id: int) -> List[Dict[str, Any]]:
    resp = requests.get(_url(f"/quiz/questions/{question_id}/answers"), headers=_auth_headers(), timeout=10)
    return _handle_response(resp)


def submit_answer(question_id: int, selected_answer_id: int, time_spent: Optional[int] = None) -> Dict[str, Any]:
    resp = requests.post(
        _url("/quiz/submit-answer"),
        headers=_auth_headers(),
        json={
            "question_id": question_id,
            "selected_answer_id": selected_answer_id,
            "time_spent": time_spent,
        },
        timeout=10,
    )
    return _handle_response(resp)


def get_statistics(subject: Optional[str] = None) -> Dict[str, Any]:
    params = {"subject": subject} if subject else {}
    resp = requests.get(_url("/quiz/statistics"), headers=_auth_headers(), params=params, timeout=10)
    return _handle_response(resp)


def get_recommendations(limit: int = 3) -> List[str]:
    resp = requests.get(_url("/quiz/recommendations"), headers=_auth_headers(), params={"limit": limit}, timeout=10)
    return _handle_response(resp)


def create_question(question_text: str, theme: str, subject: str, answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    resp = requests.post(
        _url("/quiz/questions"),
        headers=_auth_headers(),
        json={
            "question_text": question_text,
            "theme": theme,
            "subject": subject,
            "answers": answers,
        },
        timeout=10,
    )
    return _handle_response(resp)
