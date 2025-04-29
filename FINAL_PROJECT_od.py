
# +++++++++++++++++++++++++++++++++++++++++++++++
import os
from pathlib import Path
import mysql.connector
import dotenv
from mysql.connector import ProgrammingError
from datetime import datetime
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from film_by_keyword import find_film_by_keyword
from additional import get_query_type, ask_film_keyword
from film_by_genre_year import (get_list_categories,
                                     find_film_by_genre
                                     , get_max_min_year
                                     , find_film_by_genre_year
                                     , choose_category )
from popular_search_query import get_popular_search_query
# +++++++++++++++++++++++++++++++++++++++++++++++
l = 65                              # Заполнитель для разделителя блоков вывода в консоли.
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
except ProgrammingError as err:
    if err.errno == 1049:
        notice = f'\033[31m ERROR\033[m'
        print(f'{'':><{l}}\n{notice:15}'
              f' Database named \033[31m{DB_read}\033[m not found. Check the database name.'
              f'\n{'':><{l}}')
    else:
        print("Unexpected error: {}".format(err))
    exit()

# Создание объекта курсора для выполнения SQL-запросов из sakila на чтение:
cursor_read = conn_read.cursor()



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
# # <<< ---------------------------------------------------- >>>



# --------------------------------------------------------------------- #
#       2. Запись результата в БД со Счетчиком поисковых запросов       #
# --------------------------------------------------------------------- #

def write_count_query(film_keyword, category_name, film_year):
    # Дата и время запроса:
    date_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Отправка в БД group_111124_fp_Dvornyk_Olha:
    #       1) типа запроса,
    #       2) его результата,
    #       3) счетчика,
    #       4) даты и времени:
    # Вызов функции поиска фильмов по КЛЮЧЕВОМУ СЛОВУ без вывода в консоль:
    if film_keyword != '' and category_name == '' and film_year == '':
        # Создание объекта курсора на ЗАПИСЬ в БД +++
        # Создание и Обновление счётчика запросов:
        #   search_type -    %s or {0} - get_query_type('kw'),
        #   search_content - %s or {1} - film_keyword,
        #   date_time -      %s or {2} - date_time_now
        # Присваиваю тип запроса:
        # print(get_query_type('kw'))
        data_query = (get_query_type('kw'), film_keyword, date_time_now)
        cursor_write.execute(queries.get('counter_query'), data_query)
    # Вызов функции поиска фильмов по ЖАНРУ без вывода в консоль:
    if film_keyword == '' and category_name != '' and film_year == '':
        # Присваиваю тип запроса:
        # print(get_query_type('g'))
        data_query = (get_query_type('g'), category_name, date_time_now)
        cursor_write.execute(queries.get('counter_query'), data_query)
    # # Вызов функции поиска фильмов по ЖАНРУ и ГОДУ без вывода в консоль:
    if film_keyword == '' and category_name != '' and film_year != '':
    #     # Присваиваю тип запроса:
    #     # print(get_query_type('g_y'))
        data_query = (get_query_type('g_y'), f'{category_name}, {film_year}', date_time_now)
        cursor_write.execute(queries.get('counter_query'), data_query)
    conn_write.commit()

# write_count_query()



# %%%%%%%%%______    MENU    ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def main_menu():
    print(f'\033[40;32m{' ▷▷▷▷▷▷   Welcome to FILM SEARCH   ':◁<{l}}\033[0m')
    print(f'\033[40;38m{'    You can find here films by keywords, genre and year': <{l}}\033[m')
    print(f'\033[40;38m{'    Also see the most popular films in the search': <{l}}\033[m')

    while True:

        print(f'\n \033[32m▹\033[m To search for films, select the NUMBER one of the menu items:')
        print(f'\033[40;32m{' ▹▹▹▹▹▹   MENU   ':◃<{l}}\033[m')

        print(f'\033[40;32m   ▹ 1  \033[m\033[0;38m{' Search by keyword': <{l-4}}\033[m')
        print(f'\033[40;32m   ▹ 2  \033[m\033[0;38m{' Search by genre': <{l-4}}\033[m')
        print(f'\033[40;32m   ▹ 3  \033[m\033[0;38m{' Search by genre and year': <{l-4}}\033[m')
        print(f'\033[40;32m   ▹ 4  \033[m\033[0;38m{' Most POPULAR search query': <{l-4}}\033[m')
        print(f'\033[40;32m   ▹ 5  \033[m\033[0;38m{' EXIT': <{l-4}}\033[m')

        ask = input(f' Enter the \033[40;32m{' NUMBER '}\033[m of the menu items: ')
        # ask = '6'         # Так можно только для EXIT, потому что там есть break.
        if ask == '1':
            print(f'\n\033[40;32m {'':∵<{l}}\033[m'
                  f'\n\033[40;32m{'         Searching by KEYWORD ': <{l}}\033[m')
            film_keyword = ask_film_keyword()
            find_film_by_keyword(cursor_read, film_keyword)
            write_count_query(film_keyword, '', '')
        elif ask == '2':
            print(f'\n\033[40;32m{'':∵<{l}}\033[m'
                  f'\n\033[40;32m{'         Film GENRES ': <{l}}\033[m')
            print(f'\n \033[32m▹\033[m To find for films, select the NUMBER of GENRE:')
            get_list_categories(cursor_read)
            category_name = choose_category(cursor_read)
            find_film_by_genre(cursor_read, category_name)
            write_count_query('', category_name, '')
        elif ask == '3':
            print(f'\n\033[40;32m{'':∵<{l}}\033[m'
                  f'\n\033[40;32m{'         Film GENRES and YEARS': <{l}}\033[m')
            print(f'\n \033[32m▹\033[m To find for films, select the NUMBER of GENRE:')
            get_list_categories(cursor_read)
            category_name = choose_category(cursor_read)
            print(f'\n ▹ Chose the year from next range:')
            years_list = get_max_min_year(cursor_read)
            while True:
                try:
                    film_year = int(input(' Enter the YEAR from the range above: '))
                    # film_year = '1990'
                    if film_year not in years_list:
                        print('Choose the YEAR from the range above.')
                    else:
                        find_film_by_genre_year(cursor_read, category_name, film_year)
                        write_count_query('', category_name, film_year)
                        break
                except ValueError:
                    notice = f' \033[40;38m SORRY \033[m'
                    print(f'\n{notice} You should use the NUMBERS for year. Try it again.')
        elif ask == '4':
            print(f'\n\033[40;32m{'':∵<{l}}\033[m'
                  f'\n\033[40;32m{'         Popular search queries': <{l}}\033[m')
            get_popular_search_query(cursor_write)
        elif ask == '5':
            print(f'\n\033[40;32m{' ▷▷▷▷▷▷  Exiting program  ':◁<{l}}\033[m')
            print(f'\033[40;38m{'        Thank you for using our service FILM SEARCH  ': <{l}}\033[m')
            break
        else:
            print('Invalid ask, try again.')

main_menu()

# Закрытие курсора и соединения с БД на ЗАПИСЬ и ЧТЕНИЕ:
cursor_write.close()
conn_write.close()
cursor_read.close()
conn_read.close()
