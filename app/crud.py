from sqlalchemy.future import select
from sqlalchemy import or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import User, Test, Question
from schemas import UserCreate, TestCreate, QuestionCreate
import bcrypt
from typing import List, Optional


class UserCRUD:
    @staticmethod
    async def get_by_username_or_email(db: AsyncSession, username: str = None, email: str = None) -> Optional[User]:
        if not username and not email:
            return None

        query = select(User).where(or_(
            User.username == username,
            User.email == email
        ))
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate) -> User:
        hashed_password = bcrypt.hashpw(
            user_data.password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def authenticate(db: AsyncSession, username: str, password: str) -> Optional[User]:
        user = await UserCRUD.get_by_username_or_email(db, username=username)
        if not user:
            return None

        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return user
        return None


class TestCRUD:
    @staticmethod
    async def create(db: AsyncSession, user_id: int, category: str, question_count: int) -> Test:
        query = select(Question.id).where(
            Question.category == category,
            Question.is_approved == True
        ).order_by(func.random()).limit(question_count)

        result = await db.execute(query)
        question_ids = result.scalars().all()

        new_test = Test(
            user_id=user_id,
            question_ids=question_ids,
            category=category,
            total_questions=len(question_ids)
        )

        db.add(new_test)
        await db.commit()
        await db.refresh(new_test)
        return new_test

    @staticmethod
    async def get_by_id(db: AsyncSession, test_id: int) -> Optional[Test]:
        result = await db.execute(select(Test).where(Test.id == test_id))
        return result.scalars().first()

    @staticmethod
    async def get_by_criteria(
            db: AsyncSession,
            user_id: Optional[int] = None,
            category: Optional[str] = None,
            questions_count: Optional[int] = None
    ) -> List[Test]:
        query = select(Test)

        filters = []
        if user_id is not None:
            filters.append(Test.user_id == user_id)
        if category is not None:
            filters.append(Test.category == category)
        if questions_count is not None:
            filters.append(Test.total_questions == questions_count)

        query = query.where(*filters)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_test_stats(db: AsyncSession, test_id: int, new_correct_answers: int) -> Optional[Test]:
        test = await TestCRUD.get_by_id(db, test_id)
        test.update_stats(new_correct_answers)
        await db.commit()
        await db.refresh(test)
        return test


class QuestionCRUD:
    @staticmethod
    async def get_by_id(db: AsyncSession, question_id: int) -> Optional[Question]:
        result = await db.execute(select(Question).where(Question.id == question_id))
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, question_data: QuestionCreate, creator_id: int) -> Question:
        new_question = Question(
            question_text=question_data.question_text,
            options=question_data.options,
            correct_index=question_data.correct_index,
            category=question_data.category,
            created_by=creator_id
        )

        db.add(new_question)
        await db.commit()
        await db.refresh(new_question)
        return new_question

    @staticmethod
    async def approve_question(db: AsyncSession, question_id: int, approve: bool = True) -> Question:
        question = await QuestionCRUD.get_by_id(db, question_id)
        if not question:
            return None

        question.is_approved = approve

        await db.commit()
        await db.refresh(question)
        return question
