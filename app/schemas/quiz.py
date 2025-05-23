from pydantic import BaseModel
from typing import List, Optional

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