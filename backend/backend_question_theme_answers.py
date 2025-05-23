import psycopg2
import random
def connect_db():
    return psycopg2.connect(
        dbname="questiondb",
        user="postgres",
        password="652831",
        host="localhost",
        port=5432
    )


def select_themes(conn, subject):
    with conn.cursor() as cur:
        # Получаем темы с количеством вопросов
        cur.execute("""
            SELECT theme, COUNT(*) as question_count 
            FROM questions 
            WHERE subject = %s 
            GROUP BY theme;
        """, (subject,))
        themes_data = cur.fetchall()

        print("\nДоступные темы:")
        for theme, count in themes_data:
            print(f"- {theme} ({count} вопросов)")

        selected = input("\nВыберите темы (через запятую): ").strip().split(',')
        selected = [t.strip() for t in selected]

        # Проверка корректности выбора
        valid_themes = [t[0] for t in themes_data]
        invalid = [t for t in selected if t not in valid_themes]

        if invalid:
            print(f"Ошибка: темы {invalid} не найдены.")
            return select_themes(conn, subject)

        return selected

def select_subject(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT subject FROM questions;")
        subjects = [row[0] for row in cur.fetchall()]
        print("Доступные предметы:", ", ".join(subjects))
        subject = input("Выберите предмет: ").strip()
        while subject not in subjects:
            print("Ошибка: предмет не найден.")
            subject = input("Выберите предмет: ").strip()
        return subject


def get_questions(conn, subject, account_id, selected_themes):
    with conn.cursor() as cur:
        # Режим выбора тем
        if selected_themes:
            # Проверяем общее количество вопросов
            cur.execute("""
                SELECT COUNT(*) 
                FROM questions 
                WHERE subject = %s AND theme = ANY(%s)
            """, (subject, selected_themes))
            total_questions = cur.fetchone()[0]

            # Если выбрана одна тема и вопросов меньше 10
            if len(selected_themes) == 1 and total_questions < 10:
                limit = total_questions
            else:
                limit = 9

            query = """
                SELECT question_id, question_text, theme 
                FROM questions 
                WHERE subject = %s AND theme = ANY(%s)
                ORDER BY RANDOM()
                LIMIT %s;
            """
            cur.execute(query, (subject, selected_themes, limit))
            return cur.fetchall()


def save_answer(conn, account_id, question_id, selected_answer_id):
    with conn.cursor() as cur:
        cur.execute(f"""
            INSERT INTO history (test_date, account_id, question_id, result)
            SELECT 
                NOW(), 
                {account_id}, 
                {question_id}, 
                EXISTS (
                    SELECT 1 
                    FROM answers 
                    WHERE 
                        question_id = {question_id} 
                        AND answer_id = {selected_answer_id}
                        AND is_correct = true
                );
        """)
        conn.commit()


def run_testing(conn, subject, account_id, selected_themes):
    while True:
        questions = get_questions(conn, subject, account_id, selected_themes)
        if not questions:
            print("Нет доступных вопросов.")
            break

        for q in questions:
            question_id, question_text, _ = q
            print(f"\nВопрос: {question_text}")

            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM get_answers_by_question({question_id});")
                answers = cur.fetchall()
                random.shuffle(answers)
                for idx, ans in enumerate(answers, start=1):
                    print(f"{idx}. {ans[1]}")

                selected_idx = int(input("Введите номер ответа: "))
                selected_answer_id = answers[selected_idx - 1][0]  # ans[0] - answer_id
                save_answer(conn, account_id, question_id, selected_answer_id)


        # Проверка на продолжение
        choice = input("\nПродолжить тестирование? (да/нет): ").strip().lower()
        if choice != 'да':
            break


def show_statistics(conn, subject, account_id):
    with conn.cursor() as cur:
        # Общее количество уникальных вопросов, на которые отвечал пользователь
        cur.execute(f"""
            SELECT COUNT(DISTINCT h.question_id)
            FROM history h
            JOIN questions q ON h.question_id = q.question_id
            WHERE h.account_id = {account_id} AND q.subject = '{subject}';
        """)
        total_questions = cur.fetchone()[0] or 0

        # Общее количество правильных ответов (учитывая уникальные вопросы)
        cur.execute(f"""
            SELECT COUNT(DISTINCT h.question_id)
            FROM history h
            JOIN questions q ON h.question_id = q.question_id
            WHERE h.account_id = {account_id} 
                AND q.subject = '{subject}'
                AND h.result = true;
        """)
        correct_answers = cur.fetchone()[0] or 0

        # Статистика по темам
        cur.execute(f"""
            SELECT 
                q.theme,
                COUNT(DISTINCT h.question_id) FILTER (WHERE h.result = true) AS correct,
                COUNT(DISTINCT h.question_id) AS total
            FROM history h
            JOIN questions q ON h.question_id = q.question_id
            WHERE h.account_id = {account_id} AND q.subject = '{subject}'
            GROUP BY q.theme;
        """)
        stats = cur.fetchall()

        print("\nСтатистика:")
        if total_questions == 0:
            print("Нет данных для отображения.")
            return

        print(f"Всего вопросов: {total_questions}")
        print(f"Правильных ответов: {correct_answers} ({correct_answers/total_questions:.0%})\n")

        print("Детализация по темам:")
        for theme, correct, total in stats:
            print(f"- {theme}: {correct} из {total} ({correct/total:.0%})")


def main():
    conn = connect_db()

    # Аутентификация пользователя
    while True:
        username = input("Введите логин: ").strip()
        password = input("Введите пароль: ").strip()

        with conn.cursor() as cur:
            cur.execute("SELECT account_id, password FROM accounts WHERE account_name = %s", (username,))
            account_data = cur.fetchone()

            if not account_data:
                print("Ошибка: пользователь не найден")
                continue

            stored_password = account_data[1]
            if password != stored_password:  # В реальном проекте используйте хэширование!
                print("Ошибка: неверный пароль")
                continue

            account_id = account_data[0]
            break

    # Выбор предмета
    subject = select_subject(conn)

    # Выбор режима тестирования
    selected_themes = []
    theme_choice = input("\nХотите выбрать конкретные темы? (да/нет): ").strip().lower()
    if theme_choice == 'да':
        selected_themes = select_themes(conn, subject)

        # Проверка количества вопросов для одной темы
        if len(selected_themes) == 1:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT COUNT(*) FROM questions WHERE subject = %s AND theme = %s",
                    (subject, selected_themes[0])
                )
                question_count = cur.fetchone()[0]

                if question_count < 10:
                    print(f"\nВнимание: в теме '{selected_themes[0]}' только {question_count} вопросов. "
                          f"Будет показано все доступное.")

    # Запуск тестирования
    run_testing(conn, subject, account_id, selected_themes)

    # Показ статистики
    show_statistics(conn, subject, account_id)

    # Закрытие соединения
    conn.close()


if __name__ == "__main__":
    main()