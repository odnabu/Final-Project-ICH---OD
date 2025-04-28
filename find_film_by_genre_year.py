
# %%%%%%%%%______ ЧТЕНИЕ данных с БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++++++++++++++++++++++++++++++++++++++
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from decor import (print_one_field_as_table,
                   column_title_film)
from find_film_by_key_word import get_query_type
# +++++++++++++++++++++++++++++++++++++++++++++++


# --------------------------------------------------------------------- #
#       1.2. Искать фильмы: По жанру И году (10+ результатов)           #
# --------------------------------------------------------------------- #

# film_genre = int(input('To choose the category enter the number from the list above: '))
film_genre = 13



def find_film_by_genre(cursor, category_name, print_results=True):
    # Печать результатов, если print_results=True:
    if print_results is True:
        global film_genre #, category_name
        cursor.execute(queries.get('query_category_list'))
        categories = cursor.fetchall()
        if film_genre > len(categories) or film_genre < 1:
            print('Choose the number from the list above.')
        else:
            # print(category_name)      # Имя категории, которое соответствует выбранному номеру.
            cursor.execute(queries.get('query_film_by_genre'), (category_name, 'title'))
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
                print_one_field_as_table(get_query_type('g'), column_title_film, numbered_rows[start:end])
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


