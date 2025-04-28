
# %%%%%%%%%______ ЗАПИСЬ результата запроса в БД group_111124_fp_Dvornyk_Olha ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++++++++++++++++++++++++++++++++++++++
import os
from pathlib import Path
import mysql.connector
import dotenv
from datetime import datetime
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from additional import get_query_type, film_keyword
# +++++++++++++++++++++++++++++++++++++++++++++++



# %%%%%%%%%______ ПОДКЛЮЧЕНИЕ БД на ЗАПИСЬ group_111124_fp_Dvornyk_Olha ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Конфиг для подключения к серверу ich-edit:
db_config_write = {
    'host': os.environ.get("host_write"),
    'user': os.environ.get("user_write"),
    'password': os.environ.get("password_write") }
    # 'database': '___ created DB ___'}

# Подключение к серверу ich-edit:
conn_write = mysql.connector.connect(**db_config_write)
# # <<< ДЛЯ МЕНЯ >>> - выведение сообщения об успешном соединении с БД:
# print(db_config_write.get('host').split('.')[0])
# print(f'\033[40;32m{' ¨¨¨   Connection to'} \"{db_config_write.get('host').split('.')[0]}\" {'server successful!  ':¨<{l}}\033[0m')

# Создание объекта курсора для выполнения SQL-запросов в / из подключения ich-edit на запись-чтение:
cursor_write = conn_write.cursor()

# Создание БД group_111124_fp_Dvornyk_Olha если НЕ существует:
DB_write = 'group_111124_fp_Dvornyk_Olha'
cursor_write.execute(queries.get('query_create_db').format(DB_write))
# Считаю, что выводить сообщение о том, что БД успешно создана или уже существует, НЕ нужно, тк
# этот функционал НЕ для пользователя.

cursor_write.execute(queries.get('query_use_db_wr').format(DB_write))
table_for_saving = 'search_queries'
cursor_write.execute(queries.get('query_create_table').format(table_for_saving))

# # <<< ДЛЯ МЕНЯ >>> - просмотр информации о созданной таблице:
# cursor_write.execute(queries.get('query_show_creat_tb').format(table_for_saving))
# # Для вывода информации О ТАБЛИЦЕ из БД нужно использовать cursor_.fetchall():
# show_create_table = cursor_write.fetchall()
# for item in show_create_table[0]:
#     print(item)
# # <<< -------------------------------------- >>>



# --------------------------------------------------------------------- #
#       2. Запись результата в БД со Счетчиком поисковых запросов       #
# --------------------------------------------------------------------- #
def write_count_query(cursor):
    # global film_keyword
    # film_keyword = str(ask_film_keyword())
    film_kw = film_keyword
    # Дата и время запроса:
    date_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Отправка в БД group_111124_fp_Dvornyk_Olha:
    #       1) типа запроса,
    #       2) его результата,
    #       3) счетчика,
    #       4) даты и времени:
    # Вызов функции поиска фильмов по КЛЮЧЕВОМУ СЛОВУ без вывода в консоль:
    print(f'\033[31m_______________ {film_kw} ____________\033[m')
    if film_kw != '':
        # Создание объекта курсора на ЗАПИСЬ в БД +++
        # Создание и Обновление счётчика запросов:
        #   search_type -    %s or {0} - get_query_type('kw'),
        #   search_content - %s or {1} - film_keyword,
        #   date_time -      %s or {2} - date_time_now
        # Присваиваю тип запроса:
        # print(get_query_type('kw'))
        data_query = (get_query_type('kw'), film_kw, date_time_now)
        print(f'\033[31m_______________ {data_query} ____________\033[m')
        cursor.execute(queries.get('counter_query'), data_query)
    # # Вызов функции поиска фильмов по ЖАНРУ без вывода в консоль:
    # if category_name != '':
    #     # # Дата и время запроса:
    #     # date_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     # Присваиваю тип запроса:
    #     # print(get_query_type('g'))
    #     data_query = (get_query_type('g'), category_name, date_time_now)
    #     cursor_write.execute(queries.get('counter_query'), data_query)
    # # Вызов функции поиска фильмов по ЖАНРУ и ГОДУ без вывода в консоль:
    # if category_name != '' and film_year != '':
    #     # Присваиваю тип запроса:
    #     # print(get_query_type('g_y'))
    #     data_query = (get_query_type('g_y'), f'{category_name}, {film_year}', date_time_now)
    #     cursor_write.execute(queries.get('counter_query'), data_query)
    conn_write.commit()

# write_count_query()
