from typing import List, Optional, Dict
from datetime import datetime
from app.db.session import get_db
from app.schemas.quiz import Question, Answer, TestResult, UserStatistics, ThemeStatistics

def get_questions(subject: Optional[str] = None, theme: Optional[str] = None) -> List[Question]:
    with get_db() as conn:
        with conn.cursor() as cur:
            query = "SELECT question_id, question_text, theme, subject FROM questions"
            params = []
            if subject or theme:
                conditions = []
                if subject:
                    conditions.append("subject = %s")
                    params.append(subject)
                if theme:
                    conditions.append("theme = %s")
                    params.append(theme)
                query += " WHERE " + " AND ".join(conditions)
            
            cur.execute(query, params)
            return [Question(
                question_id=row[0],
                question_text=row[1],
                theme=row[2],
                subject=row[3]
            ) for row in cur.fetchall()]

def get_answers(question_id: int) -> List[Answer]:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT answer_id, answer_text, is_correct, question_id FROM answers WHERE question_id = %s",
                (question_id,)
            )
            return [Answer(
                answer_id=row[0],
                answer_text=row[1],
                is_correct=row[2],
                question_id=row[3]
            ) for row in cur.fetchall()]

def save_test_result(account_id: int, result: TestResult) -> bool:
    with get_db() as conn:
        with conn.cursor() as cur:
            # Проверяем правильность ответа
            cur.execute(
                "SELECT is_correct FROM answers WHERE question_id = %s AND answer_id = %s",
                (result.question_id, result.selected_answer_id)
            )
            is_correct = cur.fetchone()[0]
            
            # Сохраняем результат с временем
            cur.execute(
                """
                INSERT INTO history (test_date, account_id, question_id, result, time_spent)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (datetime.now(), account_id, result.question_id, is_correct, result.time_spent)
            )
            conn.commit()
            return True

def get_user_statistics(account_id: int, subject: Optional[str] = None) -> UserStatistics:
    with get_db() as conn:
        with conn.cursor() as cur:
            # Общая статистика
            cur.execute("""
                SELECT 
                    COUNT(DISTINCT test_date) as total_tests,
                    COUNT(*) as total_questions,
                    SUM(CASE WHEN result = true THEN 1 ELSE 0 END) as correct_answers,
                    AVG(CASE WHEN result = true THEN 1 ELSE 0 END) as average_score,
                    SUM(time_spent) as total_time
                FROM history
                WHERE account_id = %s
            """, (account_id,))
            stats = cur.fetchone()
            
            # Рейтинг пользователя
            cur.execute("""
                WITH user_scores AS (
                    SELECT 
                        account_id,
                        AVG(CASE WHEN result = true THEN 1 ELSE 0 END) as avg_score
                    FROM history
                    GROUP BY account_id
                )
                SELECT 
                    COUNT(*) as total_users,
                    SUM(CASE WHEN avg_score > (
                        SELECT avg_score 
                        FROM user_scores 
                        WHERE account_id = %s
                    ) THEN 1 ELSE 0 END) + 1 as user_rank
                FROM user_scores
            """, (account_id,))
            rank_info = cur.fetchone()
            
            # Статистика по темам
            cur.execute("""
                SELECT 
                    q.theme,
                    COUNT(*) as total_questions,
                    SUM(CASE WHEN h.result = true THEN 1 ELSE 0 END) as correct_answers,
                    AVG(h.time_spent) as avg_time,
                    MAX(h.test_date) as last_test
                FROM history h
                JOIN questions q ON h.question_id = q.question_id
                WHERE h.account_id = %s
                GROUP BY q.theme
                ORDER BY 
                    CASE WHEN h.result = true THEN 1 ELSE 0 END / COUNT(*) ASC
            """, (account_id,))
            theme_stats = cur.fetchall()
            
            # Определяем слабые и сильные темы
            weak_themes = [row[0] for row in theme_stats if row[2]/row[1] < 0.6]
            strong_themes = [row[0] for row in theme_stats if row[2]/row[1] >= 0.8]
            
            # Последние результаты
            cur.execute("""
                SELECT 
                    h.test_date,
                    q.theme,
                    h.result,
                    h.time_spent
                FROM history h
                JOIN questions q ON h.question_id = q.question_id
                WHERE h.account_id = %s
                ORDER BY h.test_date DESC
                LIMIT 10
            """, (account_id,))
            recent_results = [
                {
                    "date": row[0],
                    "theme": row[1],
                    "result": row[2],
                    "time_spent": row[3]
                }
                for row in cur.fetchall()
            ]
            
            return UserStatistics(
                total_tests=stats[0],
                total_questions=stats[1],
                correct_answers=stats[2],
                average_score=float(stats[3]),
                rank=rank_info[1],
                total_users=rank_info[0],
                weak_themes=weak_themes,
                strong_themes=strong_themes,
                recent_results=recent_results,
                time_spent=stats[4] or 0
            )

def get_theme_statistics(account_id: int, theme: str) -> ThemeStatistics:
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_questions,
                    SUM(CASE WHEN h.result = true THEN 1 ELSE 0 END) as correct_answers,
                    AVG(h.time_spent) as avg_time,
                    MAX(h.test_date) as last_test
                FROM history h
                JOIN questions q ON h.question_id = q.question_id
                WHERE h.account_id = %s AND q.theme = %s
            """, (account_id, theme))
            stats = cur.fetchone()
            
            return ThemeStatistics(
                theme=theme,
                total_questions=stats[0],
                correct_answers=stats[1],
                average_time=float(stats[2]) if stats[2] else 0,
                last_test_date=stats[3]
            )

def get_recommended_themes(account_id: int, limit: int = 3) -> List[str]:
    with get_db() as conn:
        with conn.cursor() as cur:
            # Сначала проверяем, есть ли у пользователя история ответов
            cur.execute("""
                SELECT COUNT(*) 
                FROM history 
                WHERE account_id = %s
            """, (account_id,))
            has_history = cur.fetchone()[0] > 0

            if has_history:
                # Если есть история, рекомендуем темы с худшими результатами
                cur.execute("""
                    SELECT 
                        q.theme,
                        COUNT(*) as total_questions,
                        SUM(CASE WHEN h.result = true THEN 1 ELSE 0 END) as correct_answers
                    FROM history h
                    JOIN questions q ON h.question_id = q.question_id
                    WHERE h.account_id = %s
                    GROUP BY q.theme
                    ORDER BY 
                        CASE WHEN h.result = true THEN 1 ELSE 0 END / NULLIF(COUNT(*), 0) ASC
                    LIMIT %s
                """, (account_id, limit))
            else:
                # Если истории нет, рекомендуем темы с наибольшим количеством вопросов
                cur.execute("""
                    SELECT 
                        theme,
                        COUNT(*) as question_count
                    FROM questions
                    GROUP BY theme
                    ORDER BY question_count DESC
                    LIMIT %s
                """, (limit,))
            
            return [row[0] for row in cur.fetchall()] 