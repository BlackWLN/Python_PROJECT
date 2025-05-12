-- Удаление БД questiondb если она существует
DROP DATABASE IF EXISTS questiondb;

-- Создание БД questiondb
--CREATE DATABASE questiondb WITH ENCODING = 'UTF8' LOCALE = 'ru_RU.UTF-8';
CREATE DATABASE questiondb;

-- Поодключение к БД questiondb
\c questiondb

-- Создание таблиц в БД questiondb
-- Таблица вопросов
CREATE TABLE questions
    (
        question_id SERIAL PRIMARY KEY,     -- идентификатор вопроса
        question_text TEXT NOT NULL,        -- текст вопроса
        theme VARCHAR(50) NOT NULL,         -- тема вопроса
        subject VARCHAR(50) NOT NULL        -- предмет
    );

-- Таблица ответов на вопросы
CREATE TABLE answers
    (
        answer_id INT NOT NULL,             -- идентификатор ответа (для каждого вопроса начинается с 1)
        answer_text TEXT NOT NULL,          -- текст ответа
        is_correct BOOLEAN NOT NULL,        -- правильность ответа
        question_id INT NOT NULL            -- идентификатор вопроса к которому отностится ответ
    );

-- Таблица с результатами тестов
CREATE TABLE history
    (
        test_date TIMESTAMP NOT NULL,       -- дата и время теста
        account_id INT NOT NULL,            -- идентификатор пользователя сдавшего тест
        question_id INT NOT NULL,           -- идентификатор вопроса
        result BOOLEAN NOT NULL,            -- правильный/неправильный дан ответ на вопрос
        time_spent INT                      -- время в секундах, потраченное на ответ
    );

-- Таблица с пользователями системы
CREATE TABLE accounts
(
    account_id SERIAL PRIMARY KEY,             -- идентификатор пользователя
    account_name VARCHAR(50) NOT NULL,         -- имя пользователя
    email VARCHAR(100) UNIQUE NOT NULL,        -- электронная почта
    password VARCHAR(100) NOT NULL             -- хэш-значение пароля
);