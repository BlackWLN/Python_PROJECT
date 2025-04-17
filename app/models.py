from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    tests = relationship("Test", back_populates="user")
    created_questions = relationship("Question", back_populates="creator")


class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    question_ids = Column(MutableList.as_mutable(PG_ARRAY(Integer)))
    category = Column(String)
    total_questions = Column(Integer)
    correct_answers = Column(Integer, default=0)
    score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="tests")

    def update_stats(self, col_correct: int):
        self.correct_answers = col_correct
        self.score = (self.correct_answers / self.total_questions) * 100
        self.completed_at = func.now()


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    options = Column(MutableList.as_mutable(PG_ARRAY(String)))
    correct_index = Column(Integer)
    category = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))
    is_approved = Column(Boolean, default=False)

    creator = relationship("User", back_populates="created_questions")
