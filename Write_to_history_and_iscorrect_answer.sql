-- Для ручного выполнения в psql (пример с конкретными значениями)
INSERT INTO history (test_date, account_id, question_id, result)
SELECT 
    NOW(), 
    1,  -- account_id 
    5,  -- question_id 
    EXISTS (
        SELECT 1 
        FROM answers 
        WHERE 
            question_id = 5 
            AND answer_id = 2  -- selected_answer_id
            AND is_correct = true
    );