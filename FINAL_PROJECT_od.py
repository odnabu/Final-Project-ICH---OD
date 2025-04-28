
# +++++++++++++++++++++++++++++++++++++++++++++++
import os
from pathlib import Path
import mysql.connector
import dotenv
from mysql.connector import ProgrammingError
from datetime import datetime
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from decor import print_one_field_as_table, column_title_film, column_title_genre, column_title_year
from find_film_by_key_word import find_film_by_key_word, get_query_type, ask_film_key_word  #, film_key_word
from find_film_by_genre_year import find_film_by_genre, film_genre
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
    print(f'\033[40;32m{' ∴∴∴   Welcome to FILM SEARCH   ':∴<{l}}\033[0m')
    print(f'\033[40;32m \\\\\\\\\\ ___   Here appears INFO and the MENU  ___//////////\033[m')
except ProgrammingError as err:
    if err.errno == 1049:
        notice = f'\033[31mERROR\033[m'
        print(f'{'':><{l}}\n{notice:15}'
              f'Database named \033[31m{DB_read}\033[m not found. Check the database name.'
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
# # <<< -------------------------------------- >>>



# %%%%%%%%%______    MENU    ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def main_menu():
    while True:
        print('\nTo search for FILMS, select th NUMBER one of the menu items:')
        print(f'\033[40;33m{'∷∷∷   MENU   ':∷<{l}}\033[m')
        # 1) To continue of the list
        # 2) Return to film search by keyword
        # 3) Search by genre and year

        print(f'\033[0;33m   ∷ 1\033[m\033[0;38m{' Search by key word': <{l-4}}\033[m')
        print(f'\033[0;33m   ∷ 2\033[m\033[0;38m{' Search by genre': <{l-4}}\033[m')
        print(f'\033[0;33m   ∷ 3\033[m\033[0;38m{' Search by genre and year': <{l-4}}\033[m')
        print(f'\033[0;33m   ∷ 4\033[m\033[0;38m{' Most POPULAR search query': <{l-4}}\033[m')
        print(f'\033[0;33m   ∷ 5\033[m\033[0;38m{' ______ Back to the MAIN MENU': <{l-4}}\033[m')
        print(f'\033[0;33m   ∷ 6\033[m\033[0;38m{' EXIT': <{l-4}}\033[m')

        ask = input('Enter the NUMBER of the menu items: ')
        # ask = '6'         # Так можно только для EXIT, потому что там есть break.
        if ask == '1':
            ask_film_key_word()
            find_film_by_key_word(cursor_read, print_results=True)
        elif ask == '2':
            get_list_categories(cursor_read)
            find_film_by_genre(cursor_read, category_name, print_results=True)
        elif ask == '3':
            get_list_categories(cursor_read)
            get_max_min_year(cursor_read)
            find_film_by_genre_year(cursor_read, print_results=True)
        elif ask == '4':
            print(f'___ 4 - not ready - the most POPULAR search query _________')
        elif ask == '5':
            print(f'__________ Back to the main menu')
            main_menu()
        elif ask == '6':
            print(f'\033[40;32m{' ∵∵∵  Exiting program  ':∵<{l}}\033[m')
            print(f'\033[40;38m{'      Thank you for using our service FILM SEARCH  ': <{l}}\033[m')
            break
        else:
            print('Invalid ask, try again.')

main_menu()



# %%%%%%%%%______ ЧТЕНИЕ данных с БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# --------------------------------------------------------------------- #
#       1.1. Искать фильмы: По ключевому слову (10+ результатов)        #
# --------------------------------------------------------------------- #
# find_film_by_key_word(cursor_read, print_results=True)



# --------------------------------------------------------------------- #
#       1.2. Искать фильмы: По жанру И году (10+ результатов)           #
# --------------------------------------------------------------------- #

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ______ Список всех категорий фильмов ________________________________
print(f'\n\033[40;32m{'':∵<{l}}\033[m'
      f'\n\033[40;32m{'     Films CATEGORIES ': <{l}}\033[m')

def get_list_categories(cursor):
    # Объект для выполнения операций с БД: отправки запросов и получения результатов:
    cursor.execute(queries.get('query_category_list'))
    categories = cursor.fetchall()
    print_one_field_as_table(get_query_type('g'), column_title_genre, categories)

# get_list_categories(cursor_read)

# ______ Поиск по ЖАНРУ _______________________________________________
print(f'\033[34m/////////// To choose the category enter the number from the list above: \033[m')
cursor_read.execute(queries.get('query_category_list'))
categories = cursor_read.fetchall()
category_name = categories[film_genre][1]
# print(category_name)

# find_film_by_genre(cursor_read, category_name, print_results=True)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ______ Список всех годов фильмов ____________________________________
print(f'\n\033[40;32m{'':∵<{l}}\033[m'
      f'\n\033[40;32m{'     Films of the following YEARS ': <{l}}\033[m')

def get_max_min_year(cursor):
    # Объект для выполнения операций с БД: отправки запросов и получения результатов:
    cursor.execute(queries.get('query_film_by_year'))
    years = cursor.fetchall()
    max_year = max(years, key=lambda x: x)[0]
    min_year = min(years, key=lambda x: x)[0]
    year_range = [(min_year, max_year)]
    # print(year_range)
    print_one_field_as_table(get_query_type('y'), column_title_year, year_range)
    return year_range

# get_max_min_year(cursor_read)


print(f'\033[34m/////////// Enter the YEAR from the range: \033[m')
# film_year = int(input('Enter the YEAR: '))
film_year = 1990
# if film_year in get_max_min_year(cursor_read)[0]:
#     print('YES!')


# ______ Поиск по ЖАНРУ и ГОДУ  _______________________________________
def find_film_by_genre_year(cursor, print_results=True):
    # Печать результатов, если print_results=True:
    if print_results is True:
        global film_year
        if film_year not in get_max_min_year(cursor)[0]:
            print('Choose the YEAR from the range above.')
        else:
            cursor.execute(queries.get('query_film_by_genre_year'), (category_name, film_year, 'release_year'))
            film_result = cursor.fetchall()
            # for film in film_result:
            #     print(film)
            # Извлечение данных из результата запроса:
            numbered_rows = [(index, *row) for index, row in enumerate(film_result, start=1)]
            # Изменение написания букв в названии фильма с капса на каждое слово с большой:
            numbered_rows = [(item[0], item[1].title(), item[2], item[3]) for item in numbered_rows]
            # Продолжение печати списка фильмов (следующие 10):
            chunk_size = 10     # Количество элементов на одной странице
            start = 0           # Начальный индекс
            end = chunk_size
            while start < len(film_result):
                print(
                    f'\tFor the genre "\033[33m{category_name}\033[m" was found \033[33m{len(film_result)}\033[m films: ')
                # Вывожу текущий "пакет" данных, те первые 10 строк:
                print_one_field_as_table(get_query_type('g_y'), column_title_film, numbered_rows[start:end])
                if end >= len(film_result):
                    break
                # Спрашиваю у пользователя, продолжать ли:
                print(f'\t\033[40;33mWould you like to continue the list (y/n)?\033[m')
                # ask = input(f'\tEnter (y/n): ')
                ask = 'n'
                if ask.lower() == 'n':
                    break
                # Переходим к следующему "пакету" данных, те к следующим 10-ти:
                start += chunk_size
                end += chunk_size
            # return
    # НЕ печатать результат, НО использовать для подсчета запросов:
    if print_results is False:
        'It is for the "counter" of the "search_content" in table group_111124_fp_Dvornyk_Olha'

# find_film_by_genre_year(cursor_read, print_results=True)




# %%%%%%%%%______ ЗАПИСЬ результата запроса в БД group_111124_fp_Dvornyk_Olha ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# --------------------------------------------------------------------- #
#       2. Запись результата в БД со Счетчиком поисковых запросов       #
# --------------------------------------------------------------------- #
def write_count_query():
    film_key_word = str(ask_film_key_word())
    global category_name
    # Отправка в БД group_111124_fp_Dvornyk_Olha:
    #       1) типа запроса,
    #       2) его результата,
    #       3) счетчика,
    #       4) даты и времени:
    # Вызов функции поиска фильмов по КЛЮЧЕВОМУ СЛОВУ без вывода в консоль:
    if find_film_by_key_word(cursor_read, print_results=False) != '':
    # ////////////  Сюда в условие надо МЕНЮ писать......
    # if film_key_word:
        # Дата и время запроса:
        date_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Создание объекта курсора на ЗАПИСЬ в БД +++
        # Создание и Обновление счётчика запросов:
        #   search_type -    %s or {0} - get_query_type('kw'),
        #   search_content - %s or {1} - film_key_word,
        #   date_time -      %s or {2} - date_time_now
        # Присваиваю тип запроса:
        # print(get_query_type('kw'))
        data_query = (get_query_type('kw'), film_key_word, date_time_now)
        cursor_write.execute(queries.get('counter_query'), data_query)
        conn_write.commit()
    # Вызов функции поиска фильмов по ЖАНРУ без вывода в консоль:
    if find_film_by_genre(cursor_read, category_name, print_results=False) != '':
        # Дата и время запроса:
        date_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Присваиваю тип запроса:
        # print(get_query_type('g'))
        data_query = (get_query_type('g'), category_name, date_time_now)
        cursor_write.execute(queries.get('counter_query'), data_query)
        conn_write.commit()
    # Вызов функции поиска фильмов по ЖАНРУ и ГОДУ без вывода в консоль:
    if find_film_by_genre_year(cursor_read, print_results=False) != '':
        # Дата и время запроса:
        date_time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Присваиваю тип запроса:
        # print(get_query_type('g'))
        data_query = (get_query_type('g_y'), f'{category_name}, {film_year}', date_time_now)
        cursor_write.execute(queries.get('counter_query'), data_query)
        conn_write.commit()

write_count_query()




# ---------------------------------------------------------------
# cursor_write.execute("SELECT * FROM search_queries")
# print(cursor_write.fetchall())

# ---------------------------------------------------------------















# Закрытие курсора и соединения с БД на ЗАПИСЬ и ЧТЕНИЕ:
cursor_write.close()
conn_write.close()
cursor_read.close()
conn_read.close()
