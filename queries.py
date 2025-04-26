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

    # Запрос на поиск по ключевому слову без ограничения вывода кол-ва найденных фильмов:
    'query_film_by_key_word':
        "SELECT title, release_year, length "   #, description
        "FROM sakila.{0} "
        "WHERE title REGEXP '{1}' "
        "{2}",                            # '^{1}| {1}| {1}  --> так выведет только слова целиком.

    # Запрос на поиск по жанру и году без ограничения вывода кол-ва найденных фильмов:


    # ______ ЗАПИСЬ в БД group_111124_fp_Dvornyk_Olha ___________________________________________________________________

    # Запрос на ЗАПИСЬ запроса, его результатов и дат + Создание и Обновление СЧЁТЧИКА запросов:
    #   search_type -    %s or {0} - get_query_type('f'),
    #   search_content - %s or {1} - film_key_word,
    #   date_time -      %s or {2} - date_time
    'counter_query':
        "INSERT INTO search_queries (search_type, search_content, cnt_search, date_time) "
        "VALUES (%s, %s, 1, %s) "
        "ON DUPLICATE KEY UPDATE cnt_search = cnt_search + 1 "

}






