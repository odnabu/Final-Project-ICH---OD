# %%%%%%%%%______ ЧТЕНИЕ данных с БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++++++++++++++++++++++++++++++++++++++
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from decor import (print_one_field_as_table,
                   column_title_film)
# +++++++++++++++++++++++++++++++++++++++++++++++

# ___ Типы ПОИСКОВЫХ ЗАПРОСОВ:
#       - Film - по ключевому слову из названия фильма,
#       - Genre - по жанру,
#       - Year - по году.
def get_query_type(key):
    query_type = {'kw': 'key_word', 'g_y': 'genre_year', 'g': 'genre', 'y': 'year'}
    return query_type.get(key)
# print(get_query_type('kw'))



# --------------------------------------------------------------------- #
#       1.1. Искать фильмы: По ключевому слову (10+ результатов)        #
# --------------------------------------------------------------------- #

# ___ Ключевое слово для поисковых запросов в таблице film БД sakila:
def ask_film_key_word():
    while True:
        key_word = input('Enter the key word for searching: ').lower()
        if key_word == '':
            print('Please enter at least one symbol for the key word.')
        else:
            return key_word
        break

# film_key_word = str(ask_film_key_word())

# film_key_word = input('Enter the key word for searching: ').lower()
# film_key_word = 'hap'

def find_film_by_key_word(cursor, print_results=True):
    # Печать результатов, если print_results=True:
    if print_results is True:
        # global film_key_word
        film_key_word = str(ask_film_key_word())
        # Объект для выполнения операций с БД: отправки запросов и получения результатов:
        cursor.execute(queries.get('query_film_by_key_word'), (film_key_word,))
        film_result = cursor.fetchall()
        # Если фильмов НЕ найдено и вернулся ПУСТОЙ список:
        if not film_result:
            print(f'\tSorry :(  No films found.')
        # Извлечение данных из результата запроса:
        numbered_rows = [(index, *row) for index, row in enumerate(film_result, start=1)]
        # Изменение написания букв в названии фильма с капса на каждое слово с большой:
        numbered_rows = [(item[0], item[1].title(), item[2], item[3]) for item in numbered_rows]
        # Продолжение печати списка фильмов (следующие 10):
        chunk_size = 10         # Количество элементов на одной странице
        start = 0               # Начальный индекс
        end = chunk_size
        while start < len(film_result):
            print(f'\tFor the key word "\033[33m{film_key_word}\033[m" was found \033[33m{len(film_result)}\033[m films: ')
            # Вывожу текущий "пакет" данных, те первые 10 строк:
            print_one_field_as_table(get_query_type('kw'), column_title_film, numbered_rows[start:end])
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
        return
        # return --- здесь НЕ БЫЛ нужен сначала, тк функция НЕ выполняет вычисления или обработку данных, и НЕ ожидается
        # использовать её результат в дальнейшем. Функция просто выполняет действие, выводя на экран результат,
        # или изменяет данные, но не возвращает результат.
    # НЕ печатать результат, НО использовать для подсчета запросов:
    if print_results is False:
        'It is for the "counter" of the "search_content" in table group_111124_fp_Dvornyk_Olha'
