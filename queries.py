# %%%%%%%_____  ЗАПРОСЫ для проекта _______%%%%%%%%%%%%%

# +++++++++++++++++++++
import mysql.connector
# +++++++++++++++++++++

queries = {

    # ______ ПОДКЛЮЧЕНИЯ, СОЗДАНИЕ БД и Таблицы ___________________________________________________________________

    # Создание БД group_111124_fp_Dvornyk_Olha если НЕ существует:
    'query_create_db': 'CREATE DATABASE IF NOT EXISTS {}',

    # <<< ДЛЯ МЕНЯ >>> - просмотр информации о созданной таблице:
    'query_show_creat_tb': 'SHOW CREATE TABLE {}',

    # Создание ТАБЛИЦЫ search_queries, куда будут вноситься:
    #       1. автоматическая нумерация - id AUTO_INCREMENT,
    #       2. тип поискового запроса (film_title, genre, year) - search_type,
    #       3. содержание поискового запроса - search_content,
    #       4. счетчик количества данного поискового запроса - cnt_search
    #       5. дата и время поискового запроса - date_time.
    'query_use_db_wr': 'USE {}',
    'query_create_table':
        "CREATE TABLE IF NOT EXISTS {} ( "
        "id INT PRIMARY KEY AUTO_INCREMENT, "
        "search_type VARCHAR(50) NOT NULL, "
        "search_content VARCHAR(255) NOT NULL UNIQUE, "
        "cnt_search INT DEFAULT 1, "
        "date_time DATETIME )",          # DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP --> https://dev.mysql.com/doc/refman/8.4/en/datetime.html

    # ______ Чтение из БД sakila ___________________________________________________________________

    # Поиск по КЛЮЧЕВОМУ СЛОВУ без ограничения вывода кол-ва найденных фильмов:
    'query_film_by_keyword':
        "SELECT title, release_year, length "   #, description
        "FROM sakila.film "
        "WHERE title REGEXP %s ",     # '^{1}| {1}| {1}  --> так выведет только слова целиком.

    # Список всех категорий фильмов из таблицы category:
    'query_category_list':
    "SELECT category_id, name "
    "FROM sakila.category "
    "ORDER BY name",

    # Поиск по ЖАНРУ без ограничения вывода кол-ва найденных фильмов:
    'query_film_by_genre':
        "SELECT film.title, release_year, length " 
        "FROM sakila.film "
        "   INNER JOIN film_category ON film.film_id = film_category.film_id "
        "   INNER JOIN category ON category.category_id = film_category.category_id "
        "               AND category.name = %s "
        "ORDER BY %s",

    # Просмотр диапазона ГОДОВ фильмов:
    'query_film_by_year':
        "SELECT release_year "
        "FROM sakila.film "
        "GROUP BY release_year "
        "ORDER BY release_year DESC",          #  1990-2025

    # Поиск по ЖАНРУ и ГОДУ (одновременно) без ограничения вывода кол-ва найденных фильмов:
    'query_film_by_genre_year':
        "SELECT film.title, release_year, length "
        "FROM sakila.film "
        "	INNER JOIN film_category ON film.film_id = film_category.film_id "
        "	INNER JOIN category ON category.category_id = film_category.category_id "
        "			AND category.name = %s "
        "			AND release_year = %s "
        # "			AND release_year BETWEEN 1990 AND 1998 "
        "ORDER BY %s",

    # ______ ЗАПИСЬ в БД group_111124_fp_Dvornyk_Olha ___________________________________________________________________

    # Запрос на ЗАПИСЬ типа запроса, его результатов и дат + Создание и Обновление СЧЁТЧИКА запросов:
    #   search_type -    %s or {0} - get_query_type('kw'),
    #   search_content - %s or {1} - film_keyword,
    #   date_time -      %s or {2} - date_time
    'counter_query':
        "INSERT INTO search_queries (search_type, search_content, cnt_search, date_time) "
        "VALUES (%s, %s, 1, %s) "
        "ON DUPLICATE KEY UPDATE cnt_search = cnt_search + 1, date_time = VALUES(date_time) ",

    # ______ ЧТЕНИЕ из БД group_111124_fp_Dvornyk_Olha ___________________________________________________________________
    # Печать 3-х самых популярных запросов из таблицы search_queries:
    'popular_search_query':
        "SELECT search_type, search_content "
        "FROM group_111124_fp_Dvornyk_Olha.search_queries "
        "ORDER BY cnt_search DESC " 
        "LIMIT %s"
}






