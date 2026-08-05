from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.schemas.quiz import (
    Question, Answer, TestResult, UserStatistics,
    ThemeStatistics, TestSettings, QuestionWithAnswersCreate, SubjectThemes,
    LeaderboardEntry
)
from app.services.quiz import (
    get_questions,
    get_answers,
    save_test_result,
    get_user_statistics,
    get_theme_statistics,
    get_recommended_themes,
    get_subjects_themes,
    create_question,
    get_leaderboard
)

router = APIRouter()

@router.get("/subjects", response_model=List[SubjectThemes])
def read_subjects(current_user: dict = Depends(get_current_user)):
    """Список предметов и тем, доступных для тестирования (для выбора теста)."""
    return get_subjects_themes()

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def read_leaderboard(
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """Топ пользователей по среднему проценту правильных ответов."""
    return get_leaderboard(limit=limit)

@router.post("/questions", response_model=Question)
def create_new_question(
    question: QuestionWithAnswersCreate,
    current_user: dict = Depends(get_current_user)
):
    """Позволяет залогиненному пользователю добавить свой вопрос в банк вопросов."""
    try:
        return create_question(question)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.get("/questions", response_model=List[Question])
def read_questions(
    subject: Optional[str] = None,
    theme: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    return get_questions(subject=subject, theme=theme)

@router.get("/questions/{question_id}/answers", response_model=List[Answer])
def read_answers(
    question_id: int,
    current_user: dict = Depends(get_current_user)
):
    answers = get_answers(question_id)
    if not answers:
        raise HTTPException(status_code=404, detail="Question not found")
    return answers

@router.post("/submit-answer")
def submit_answer(
    result: TestResult,
    current_user: dict = Depends(get_current_user)
):
    success = save_test_result(current_user["account_id"], result)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to save answer")
    return {"status": "success"}

@router.get("/statistics", response_model=UserStatistics)
def read_statistics(
    subject: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    return get_user_statistics(current_user["account_id"], subject)

@router.get("/statistics/theme/{theme}", response_model=ThemeStatistics)
def read_theme_statistics(
    theme: str,
    current_user: dict = Depends(get_current_user)
):
    return get_theme_statistics(current_user["account_id"], theme)

@router.get("/recommendations", response_model=List[str])
def get_recommendations(
    limit: int = 3,
    current_user: dict = Depends(get_current_user)
):
    return get_recommended_themes(current_user["account_id"], limit)

@router.post("/start-test")
def start_test(
    settings: TestSettings,
    current_user: dict = Depends(get_current_user)
):
    # Получаем вопросы на основе настроек
    questions = get_questions(theme=settings.themes[0] if settings.themes else None)
    
    # Если включены слабые темы, добавляем вопросы из них
    if settings.include_weak_themes:
        weak_themes = get_recommended_themes(current_user["account_id"])
        for theme in weak_themes:
            if theme not in settings.themes:
                questions.extend(get_questions(theme=theme))
    
    # Ограничиваем количество вопросов на тему
    if settings.questions_per_theme:
        questions = questions[:settings.questions_per_theme]
    
    return {
        "questions": questions,
        "time_limit": settings.time_limit,
        "total_questions": len(questions)
    } 