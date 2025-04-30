import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="questiondb",
        user="postgres",
        password="652831",
        host="localhost",
        port=5432
    )

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

def get_questions(conn, subject, account_id):
    with conn.cursor() as cur:
        query = f"""
        WITH theme_stats AS (
            SELECT 
                q.theme,
                COUNT(h.result) FILTER (WHERE h.result = true) AS correct_count
            FROM questions q
            LEFT JOIN history h ON q.question_id = h.question_id AND h.account_id = {account_id}
            WHERE q.subject = '{subject}'
            GROUP BY q.theme
            ORDER BY correct_count ASC, q.theme
            LIMIT 2
        ),
        weak_questions AS (
            SELECT 
                q.question_id,
                q.question_text,
                q.theme,
                ROW_NUMBER() OVER (PARTITION BY q.theme ORDER BY RANDOM()) AS rn
            FROM questions q
            WHERE q.theme IN (SELECT theme FROM theme_stats)
        ),
        other_themes AS (
            SELECT DISTINCT theme 
            FROM questions 
            WHERE theme NOT IN (SELECT theme FROM theme_stats) AND subject = '{subject}'
        ),
        other_questions AS (
            SELECT 
                q.question_id,
                q.question_text,
                q.theme,
                ROW_NUMBER() OVER (PARTITION BY q.theme ORDER BY RANDOM()) AS rn
            FROM questions q
            WHERE q.theme IN (SELECT theme FROM other_themes)
        )
        SELECT * FROM (
            SELECT question_id, question_text, theme FROM weak_questions WHERE rn <= 3
            UNION ALL
            SELECT question_id, question_text, theme FROM other_questions WHERE rn = 1
        ) AS combined
        ORDER BY RANDOM()
        LIMIT 9;
        """
        cur.execute(query)
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


def run_testing(conn, subject, account_id):
    while True:
        questions = get_questions(conn, subject, account_id)
        if not questions:
            print("Нет доступных вопросов.")
            break

        for q in questions:
            question_id, question_text, _ = q
            print(f"\nВопрос: {question_text}")

            # Получение вариантов ответа
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM get_answers_by_question({question_id});")
                answers = cur.fetchall()
                for ans in answers:
                    print(f"{ans[0]}. {ans[1]}")

                selected = int(input("Введите номер ответа: "))
                save_answer(conn, account_id, question_id, selected)

        # Проверка на продолжение
        choice = input("\nПродолжить тестирование? (да/нет): ").strip().lower()
        if choice != 'да':
            break

def show_statistics(conn, subject, account_id):
    with conn.cursor() as cur:
        cur.execute(f"""
            SELECT 
                q.theme,
                COUNT(h.result) FILTER (WHERE h.result = true) AS correct,
                COUNT(h.result) AS total
            FROM history h
            JOIN questions q ON h.question_id = q.question_id
            WHERE h.account_id = {account_id} AND q.subject = '{subject}'
            GROUP BY q.theme;
        """)
        stats = cur.fetchall()
        print("\nСтатистика:")
        for theme, correct, total in stats:
            print(f"- {theme}: {correct} из {total}")


def main():
    conn = connect_db()

    # Аутентификация
    while True:
        username = input("Введите имя пользователя: ").strip()
        password = input("Введите пароль: ").strip()

        with conn.cursor() as cur:
            cur.execute("SELECT account_id, password FROM accounts WHERE account_name = %s", (username,))
            account_data = cur.fetchone()

            if not account_data:
                print("Ошибка: пользователь не найден")
                continue

            stored_password = account_data[1]
            if password != stored_password:  # Вообще тут надо хэширование!
                print("Ошибка: неверный пароль")
                continue

            account_id = account_data[0]
            break

    subject = select_subject(conn)
    run_testing(conn, subject, account_id)
    show_statistics(conn, subject, account_id)

    conn.close()


if __name__ == "__main__":
    main()