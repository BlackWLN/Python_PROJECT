from typing import List, Optional
from app.db.session import get_db
from app.schemas.quiz import Question, Answer, TestResult

def get_questions(subject: Optional[str] = None, theme: Optional[str] = None) -> List[Question]:
    with get_db() as conn:
        with conn.cursor() as cur:
            if subject and theme:
                cur.execute(
                    "SELECT question_id, question_text, theme, subject FROM questions WHERE subject = %s AND theme = %s",
                    (subject, theme)
                )
            elif subject:
                cur.execute(
                    "SELECT question_id, question_text, theme, subject FROM questions WHERE subject = %s",
                    (subject,)
                )
            else:
                cur.execute("SELECT question_id, question_text, theme, subject FROM questions")
            
            return [
                Question(
                    question_id=row[0],
                    question_text=row[1],
                    theme=row[2],
                    subject=row[3]
                )
                for row in cur.fetchall()
            ]

def get_answers(question_id: int) -> List[Answer]:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT answer_id, answer_text, is_correct, question_id FROM answers WHERE question_id = %s",
                (question_id,)
            )
            return [
                Answer(
                    answer_id=row[0],
                    answer_text=row[1],
                    is_correct=row[2],
                    question_id=row[3]
                )
                for row in cur.fetchall()
            ]

def save_test_result(account_id: int, result: TestResult) -> bool:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO history (test_date, account_id, question_id, result)
                SELECT 
                    NOW(), 
                    %s, 
                    %s, 
                    EXISTS (
                        SELECT 1 
                        FROM answers 
                        WHERE 
                            question_id = %s 
                            AND answer_id = %s
                            AND is_correct = true
                    )
            """, (account_id, result.question_id, result.question_id, result.selected_answer_id))
            conn.commit()
            return True

def get_user_statistics(account_id: int, subject: Optional[str] = None) -> dict:
    with get_db() as conn:
        with conn.cursor() as cur:
            if subject:
                cur.execute("""
                    SELECT 
                        q.theme,
                        COUNT(h.result) FILTER (WHERE h.result = true) AS correct,
                        COUNT(h.result) AS total
                    FROM history h
                    JOIN questions q ON h.question_id = q.question_id
                    WHERE h.account_id = %s AND q.subject = %s
                    GROUP BY q.theme
                """, (account_id, subject))
            else:
                cur.execute("""
                    SELECT 
                        q.theme,
                        COUNT(h.result) FILTER (WHERE h.result = true) AS correct,
                        COUNT(h.result) AS total
                    FROM history h
                    JOIN questions q ON h.question_id = q.question_id
                    WHERE h.account_id = %s
                    GROUP BY q.theme
                """, (account_id,))
            
            stats = cur.fetchall()
            return {
                theme: {
                    "correct": correct,
                    "total": total,
                    "percentage": (correct / total * 100) if total > 0 else 0
                }
                for theme, correct, total in stats
            } 