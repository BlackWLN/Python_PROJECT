from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuestionBase(BaseModel):
    question_text: str
    theme: str
    subject: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    question_id: int

    class Config:
        from_attributes = True

class AnswerBase(BaseModel):
    answer_text: str
    is_correct: bool
    question_id: int

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    answer_id: int

    class Config:
        from_attributes = True

class TestResult(BaseModel):
    question_id: int
    selected_answer_id: int
    time_spent: Optional[int] = None  # время в секундах

class UserStatistics(BaseModel):
    total_tests: int
    total_questions: int
    correct_answers: int
    average_score: float
    rank: int
    total_users: int
    weak_themes: List[str]
    strong_themes: List[str]
    recent_results: List[dict]
    time_spent: int  # общее время в секундах

class ThemeStatistics(BaseModel):
    theme: str
    total_questions: int
    correct_answers: int
    average_time: float
    last_test_date: Optional[datetime]

class TestSettings(BaseModel):
    themes: List[str]
    time_limit: Optional[int] = None  # общее время в секундах
    questions_per_theme: Optional[int] = None
    include_weak_themes: bool = True 