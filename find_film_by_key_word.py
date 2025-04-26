# %%%%%%%%%______ ЧТЕНИЕ данных с БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++++++++++++++++++++++++++++++++++++++
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from decor import (print_one_field_as_table,
                   column_title)
# +++++++++++++++++++++++++++++++++++++++++++++++

# ___ Типы ПОИСКОВЫХ ЗАПРОСОВ:
#       - Film - по ключевому слову из названия фильма,
#       - Genre - по жанру,
#       - Year - по году.
def get_query_type(key):
    query_type = {'f': 'Film', 'g': 'Genre', 'y': 'Year'}
    return query_type.get(key)
# print(get_query_type('f'))

table_film = 'film'
# film_key_word = input('Enter the key word for searching: ').lower()
film_key_word = 'no'



# --------------------------------------------------------------------- #
#       1.1. Искать фильмы: По ключевому слову (10+ результатов)        #
# --------------------------------------------------------------------- #

def find_film_by_key_word(cursor):
    global film_key_word
    back_to_the_menu = f"\033[31m------------- Возврат в основное меню -----------------\033[m"
    # Объект для выполнения операций с БД: отправки запросов и получения результатов:
    cursor.execute(queries.get('query_film_by_key_word').format(table_film, film_key_word, ''))
    film_result = cursor.fetchall()
    if not film_result:
        print(f'\tSorry :(  No films found.')
        print(back_to_the_menu)
    # Извлечение данных из результата запроса:
    numbered_rows = [(index, *row) for index, row in enumerate(film_result, start=1)]
    # Изменяю написание букв в названии фильма с капса на каждое слово с большой:
    numbered_rows = [(item[0], item[1].title(), item[2], item[3]) for item in numbered_rows]
    # Продолжение печати списка фильмов (следующие 10):
    chunk_size = 10         # Количество элементов на одной странице
    start = 0               # Начальный индекс
    end = chunk_size
    while start < len(film_result):
        print(f'\tFor the key word "\033[33m{film_key_word}\033[m" was found \033[33m{len(film_result)}\033[m films: ')
        # Вывожу текущий "пакет" данных:
        print_one_field_as_table(get_query_type('f'), column_title, numbered_rows[start:end])
        if end >= len(film_result):
            print(back_to_the_menu)
            break
        # Спрашиваю у пользователя, продолжать ли:
        print(f'\t\033[40;33mWould you like to continue the list (y/n)?\033[m')
        # ask = input(f'\tEnter (y/n): ')
        ask = 'n'
        if ask.lower() == 'n':
            print(back_to_the_menu)
            break
        # Переходим к следующему "пакету" данных:
        start += chunk_size
        end += chunk_size
    # return --- здесь НЕ нужен, т.к. функция НЕ выполняет вычисления или обработку данных, и НЕ ожидается
    # использовать её результат в дальнейшем. Функция просто выполняет действие, выводя на экран результат,
    # или изменяет данные, но не возвращает результат.
