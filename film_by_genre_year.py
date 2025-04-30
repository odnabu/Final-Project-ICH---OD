
# %%%%%%%%%______ ЧТЕНИЕ данных из БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++++++++++++++++++++++++++++++++++++++
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from decor import (print_one_field_as_table, column_title, header_text)
from film_by_keyword import get_query_type
# +++++++++++++++++++++++++++++++++++++++++++++++

l = 60

# --------------------------------------------------------------------- #
#       1.2. Искать фильмы: По жанру И году (10+ результатов)           #
# --------------------------------------------------------------------- #


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ______ Список всех категорий фильмов ________________________________

# print_one_field_as_table(header_text,
#                          search_type,
#                          film_keyword,
#                          column_title,
#                          data_in_col)

def get_list_categories(cursor):
    """
    Функция вывода на экран нумерованного списка категорий из таблицы category в БД sakila.
    """
    # Объект для выполнения операций с БД: отправки запросов и получения результатов:
    cursor.execute(queries.get('query_category_list'))
    category_list = cursor.fetchall()
    print_one_field_as_table(header_text.get('header_text_categor'),
                             '',
                             get_query_type('g'),
                             column_title.get('column_title_genre'),
                             category_list)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ______ Выбор ЖАНРА _______________________________________________

def choose_category(cursor):
    """
    Функция выбора пользователем категории и проверки введенного им значения:
    присутствует ли значение в таблице category БД sakila.
    """
    cursor.execute(queries.get('query_category_list'))
    categories = cursor.fetchall()
    # Список номеров жанров (категорий):
    categor_numb = [i[0] for i in categories]

    while True:
        try:
            film_genre = int(input(' ENTER the number from the list above: '))
            # film_genre = 16
            if film_genre in categor_numb:
                # Имя категории, которое соответствует выбранному номеру из списка:
                category_name = categories[film_genre - 1][1]
                return category_name
            else:
                print(f' \033[40;38m SORRY \033[m Please enter the NUMBER from the list above.')
        except ValueError:
            notice = f' \033[40;38m SORRY \033[m'
            print(f'\n   {notice} Please use NUMBERS only. Try it again.')



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ______ Поиск по ЖАНРУ _______________________________________________


def find_film_by_genre(cursor, category_name):
    """
    Функция поиска фильмов по ЖАНРУ в таблице film БД sakila с ограничением вывода в 10 строк
    и возможностью для пользователя вывести следующие 10 и т.д.
    """
    cursor.execute(queries.get('query_film_by_genre'), (category_name, 'title'))
    film_result = cursor.fetchall()

    # Если фильмов НЕ найдено и вернулся ПУСТОЙ список:
    if not film_result:
        print(f' \033[40;38m SORRY \033[m  No films found.')

    else:
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
                f'\n   For the genre "\033[33m{category_name}\033[m" was found \033[33m{len(film_result)}\033[m films: ')
            # Вывожу текущий "пакет" данных, те первые 10 строк:
            print_one_field_as_table(header_text.get('header_text_film'),
                                     get_query_type('g'),
                                     category_name,
                                     column_title.get('column_title_film'),
                                     numbered_rows[start:end])
            if end >= len(film_result):
                break
            # Спрашиваю у пользователя, продолжать ли:
            print(f'\t\033[0;37m Would you like to continue the list?\033[m')
            ask = input(f'\tEnter any key to continue or \033[0;32m"n"\033[m to stop: ')
            # ask = 'n'
            if ask.lower() == 'n':
                break
            # Переход к следующему "пакету" данных, те к следующим 10-ти:
            start += chunk_size
            end += chunk_size



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ______ Список всех годов фильмов ____________________________________

def get_max_min_year(cursor):
    """
    Функция печати минимального и максимального значений года выпуска фильмов,
    представленных в таблице film БД sakila.
    """
    # Объект для выполнения операций с БД: отправки запросов и получения результатов:
    cursor.execute(queries.get('query_film_by_year'))
    years = cursor.fetchall()
    # Список всех годов релиза фильмов:
    years_list = [y[0] for y in years]
    max_year = max(years, key=lambda x: x)[0]
    min_year = min(years, key=lambda x: x)[0]
    year_range = [(min_year, max_year)]
    print_one_field_as_table(header_text.get('header_text_max_min_year'),
                                '',
                                get_query_type('y'),
                                column_title.get('column_title_year'),
                                year_range)
    return years_list



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# ______ Поиск по ЖАНРУ и ГОДУ  _______________________________________

def find_film_by_genre_year(cursor, category_name, film_year):
    """
    Функция поиска фильмов по ЖАНРУ и ГОДУ в таблице film БД sakila с ограничением вывода в 10 строк
    и возможностью для пользователя вывести следующие 10 и т.д.
    """
    cursor.execute(queries.get('query_film_by_genre_year'), (category_name, film_year, 'release_year'))
    film_result = cursor.fetchall()

    # Если фильмов НЕ найдено и вернулся ПУСТОЙ список:
    if not film_result:
        print(f' \033[40;38m SORRY \033[m  No films found.')

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
            f'\n   For the genre "\033[33m{category_name}\033[m" was found \033[33m{len(film_result)}\033[m films: ')
        # Вывожу текущий "пакет" данных, те первые 10 строк:
        print_one_field_as_table(header_text.get('header_text_film'),
                                 get_query_type('g_y'),
                                 category_name,
                                 column_title.get('column_title_film'),
                                 numbered_rows[start:end])
        if end >= len(film_result):
            break
        # Спрашиваю у пользователя, продолжать ли:
        print(f'\t\033[0;37m Would you like to continue the list?\033[m')
        ask = input(f'\tEnter any key to continue or \033[0;32m"n"\033[m to stop: ')
        # ask = 'n'
        if ask.lower() == 'n':
            break
        # Переход к следующему "пакету" данных, те к следующим 10-ти:
        start += chunk_size
        end += chunk_size
