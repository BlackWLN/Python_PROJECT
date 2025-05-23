from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.schemas.quiz import Question, Answer, TestResult
from app.services.quiz import (
    get_questions,
    get_answers,
    save_test_result,
    get_user_statistics
)

router = APIRouter()

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

@router.get("/statistics")
def read_statistics(
    subject: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    return get_user_statistics(current_user["account_id"], subject) 