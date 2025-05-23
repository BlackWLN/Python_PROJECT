-- Создание самой фуннкции
CREATE OR REPLACE FUNCTION get_answers_by_question(question_id INT)
RETURNS TABLE (
    answer_id INT,
    answer_text TEXT,
    is_correct BOOLEAN
) AS $$
BEGIN
    RETURN QUERY
    SELECT a.answer_id, a.answer_text, a.is_correct
    FROM answers a
    WHERE a.question_id = get_answers_by_question.question_id;
END;
$$ LANGUAGE plpgsql;

WITH theme_stats AS (
    SELECT 
        q.theme,
        COUNT(h.result) FILTER (WHERE h.result = true) AS correct_count
    FROM questions q
    LEFT JOIN history h ON q.question_id = h.question_id
    WHERE q.subject = 'ФИ'
    GROUP BY q.theme
    ORDER BY correct_count ASC, q.theme
    LIMIT 2
),
-- Вопросы из слабых тем (минимум 6)
weak_questions AS (
    SELECT 
        q.question_id,
        q.question_text,
        q.theme,
        ROW_NUMBER() OVER (PARTITION BY q.theme ORDER BY RANDOM()) AS rn
    FROM questions q
    WHERE q.theme IN (SELECT theme FROM theme_stats)
),
-- Все оставшиеся темы
other_themes AS (
    SELECT DISTINCT theme 
    FROM questions 
    WHERE theme NOT IN (SELECT theme FROM theme_stats)
),
-- По 1 вопросу из каждой оставшейся темы
other_questions AS (
    SELECT 
        q.question_id,
        q.question_text,
        q.theme,
        ROW_NUMBER() OVER (PARTITION BY q.theme ORDER BY RANDOM()) AS rn
    FROM questions q
    WHERE q.theme IN (SELECT theme FROM other_themes)
)
-- Собираем итоговую выборку
SELECT * FROM (
    -- 6 вопросов из слабых тем
    SELECT question_id, question_text, theme FROM weak_questions WHERE rn <= 3
    
    UNION ALL
    
    -- По 1 вопросу из других тем (максимум 4 темы)
    SELECT question_id, question_text, theme FROM other_questions WHERE rn = 1
) AS combined
ORDER BY RANDOM()
LIMIT 10; -- Всего 10 вопросов (6+4 или больше из слабых)

-- А тут уже запускаем первую функцию, то есть выводим варианты ответов к вопросу с ID(например 5)
SELECT * FROM get_answers_by_question(5);