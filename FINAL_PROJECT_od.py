
# +++++++++++++++++++++++++++++++++++++++++++++++
import os
from pathlib import Path
import mysql.connector
import dotenv
from mysql.connector import ProgrammingError
from datetime import datetime
# ___ Вызовы из моих файлов: ___________________
from queries import queries
# from decor import print_one_field_as_table
from find_film_by_key_word import (find_film_by_key_word,
                                   get_query_type,
                                   film_key_word)
# +++++++++++++++++++++++++++++++++++++++++++++++
l = 60  # 80                        # Заполнитель для разделителя блоков вывода в консоли.
t = 5                               # Табулятор для текста.
dotenv.load_dotenv(Path('.env'))


# %%%%%%%%%______ ПОДКЛЮЧЕНИЕ БД на ЧТЕНИЕ sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Конфиг для подключения к серверу ich с базой данных sakila:
DB_read = 'sakila'
db_config_read = {
    'host': os.environ.get("host_read"),
    'user': os.environ.get("user_read"),
    'password': os.environ.get("password_read"),
    'database': DB_read}
try:
    # Подключение базы данных sakila:
    conn_read = mysql.connector.connect(**db_config_read)
    # print(f'\033[40;32m{' ∴∴∴   Welcome to FILM SEARCH   ':∴<{l}}\033[0m')
except ProgrammingError as err:
    if err.errno == 1049:
        notice = f'\033[31mERROR\033[m'
        print(f'{'':><{l}}\n{notice:15}'
              f'Database named \033[31m{DB_read}\033[m not found. Check the database name.'
              f'\n{'':><{l}}')
    else:
        print("Unexpected error: {}".format(err))
    exit()


# %%%%%%%%%______ ПОДКЛЮЧЕНИЕ БД на ЗАПИСЬ group_111124_fp_Dvornyk_Olha ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Конфиг для подключения к серверу ich-edit:
db_config_write = {
    'host': os.environ.get("host_write"),
    'user': os.environ.get("user_write"),
    'password': os.environ.get("password_write") }
    # 'database': '___ created DB ___'}

# Подключение к серверу ich-edit:
conn_write = mysql.connector.connect(**db_config_write)
# print(db_config_write.get('host').split('.')[0])
print(f'\033[40;32m{' ¨¨¨   Connection to'} \"{db_config_write.get('host').split('.')[0]}\" {'server successful!  ':¨<{l}}\033[0m')

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



# %%%%%%%%%______ ЧТЕНИЕ данных с БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Создание объекта курсора для выполнения SQL-запросов из sakila на чтение:
cursor_read = conn_read.cursor()


# --------------------------------------------------------------------- #
#       1.1. Искать фильмы: По ключевому слову (10+ результатов)        #
# --------------------------------------------------------------------- #
# find_move_by_key_word(cursor_read)


# --------------------------------------------------------------------- #
#       1.2. Искать фильмы: По жанру и году (10+ результатов)           #
# --------------------------------------------------------------------- #

table_categories = 'category'
table_film_to_category = 'film_category'

def find_film_by_genre_year(cursor):
    pass



# %%%%%%%%%______ ЗАПИСЬ результата запроса в БД group_111124_fp_Dvornyk_Olha ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# --------------------------------------------------------------------- #
#       2. Запись результата в БД со Счетчиком поисковых запросов       #
# --------------------------------------------------------------------- #
def write_count_query():
    # Отправка в БД group_111124_fp_Dvornyk_Olha:
    #       1) типа запроса,
    #       2) его результата,
    #       3) счетчика,
    #       4) даты и времени:
    if find_film_by_key_word(cursor_read) != '':
        # Присваиваю тип запроса:
        # print(get_query_type('f'))
        # Дата и время запроса:
        date_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Создание объекта курсора на ЗАПИСЬ в БД +++
        # Создание и Обновление счётчика запросов:
        #   search_type -    %s or {0} - get_query_type('f'),
        #   search_content - %s or {1} - film_key_word,
        #   date_time -      %s or {2} - date_time_now
        data_query = (get_query_type('f'), film_key_word, date_time_now)
        cursor_write.execute(queries.get('counter_query'), data_query)
        conn_write.commit()
    # return
write_count_query()


# ---------------------------------------------------------------
# cursor_write.execute("SELECT * FROM search_queries")
# print(cursor_write.fetchall())

# ---------------------------------------------------------------





# def keep_going_menu():
#     while True:
#         print(f'\033[40;33m{'___ Choose what do you want to do next:  ':_<{l}}\033[m')
#         # 1) To continue of the list
#         # 2) Return to movie search by keyword
#         # 3) Search by genre and year
#         ask = int(input(f'\033[40;33m{'Enter 1, 2 or 3: ':_<{l}}\033[m (y/n): '))
#         if ask == 1:
#
#             break
#     pass














# Закрытие курсора и соединения с БД на ЗАПИСЬ и ЧТЕНИЕ:
cursor_write.close()
conn_write.close()
cursor_read.close()
conn_read.close()
# print(f'\n\033[40;32m{' ∵∵∵  Thank you for using our service FILM SEARCH  ':∵<{l}}\033[m')