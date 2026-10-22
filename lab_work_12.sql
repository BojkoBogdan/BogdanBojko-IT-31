-- Практика 12. Варіант: кінотеатр
-- Запити не змінюють структуру бази.

-- Завдання 1: сортування за ціною квитка за спаданням
SELECT id, movie_id, hall_id, show_date, ticket_price
FROM tickets
ORDER BY ticket_price DESC;

-- Завдання 2: спочатку зал за зростанням, потім дата за спаданням
SELECT id, hall_id, show_date, ticket_price
FROM tickets
ORDER BY hall_id ASC, show_date DESC;

-- Завдання 3: три найдорожчі квитки
SELECT id, movie_id, hall_id, show_date, ticket_price
FROM tickets
ORDER BY ticket_price DESC
LIMIT 3;

-- Завдання 4а: унікальні жанри
SELECT DISTINCT genre
FROM movies
ORDER BY genre;

-- Завдання 4б: ціни від 200 до 300 включно
SELECT id, movie_id, ticket_price
FROM tickets
WHERE ticket_price BETWEEN 200 AND 300
ORDER BY ticket_price;

-- Завдання 5: LIKE з великою та малою кириличною літерою
SELECT hall_name FROM halls WHERE hall_name LIKE 'З%';
SELECT hall_name FROM halls WHERE hall_name LIKE 'з%';

-- Підрахунок для порівняння
SELECT COUNT(*) AS count_upper FROM halls WHERE hall_name LIKE 'З%';
SELECT COUNT(*) AS count_lower FROM halls WHERE hall_name LIKE 'з%';
