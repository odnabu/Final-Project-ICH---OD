# %%%%%%%%%______ ЧТЕНИЕ данных из БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++++++++++++++++++++++++++++++++++++++
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from decor import (print_one_field_as_table,
                   column_title, header_text)
from additional import get_query_type
# +++++++++++++++++++++++++++++++++++++++++++++++


# --------------------------------------------------------------------- #
#       1.1. Искать фильмы: По ключевому слову (10+ результатов)        #
# --------------------------------------------------------------------- #

# print_one_field_as_table(header_text,
#                          search_type,
#                          film_keyword,
#                          column_title,
#                          data_in_col)

def find_film_by_keyword(cursor, film_keyword):
    """
    Функция поиска фильмов по КЛЮЧЕВОМУ СЛОВУ в таблице film БД sakila с ограничением вывода в 10 строк
    и возможностью для пользователя вывести следующие 10 и т.д.
    """
    # Объект для выполнения операций с БД: отправки запросов и получения результатов:
    cursor.execute(queries.get('query_film_by_keyword'), (film_keyword,))
    film_result = cursor.fetchall()

    # Если фильмов НЕ найдено и вернулся ПУСТОЙ список:
    if not film_result:
        message = f'   No films found that contain the keyword "\033[33m{film_keyword}\033[m" in the title.'
        print(message)

    else:
        # Извлечение данных из результата запроса:
        numbered_rows = [(index, *row) for index, row in enumerate(film_result, start=1)]
        # Изменение написания букв в названии фильма с капса на каждое слово с большой:
        numbered_rows = [(item[0], item[1].title(), item[2], item[3]) for item in numbered_rows]

        # Продолжение печати списка фильмов (следующие 10):
        chunk_size = 10         # Количество элементов на одной странице
        start = 0               # Начальный индекс
        end = chunk_size

        message = f'\n   For the keyword "\033[33m{film_keyword}\033[m" was found \033[33m{len(film_result)}\033[m films: '
        print(message)
        while start < len(film_result):
            # Вывожу текущий "пакет" данных, те первые 10 строк:
            print_one_field_as_table(header_text.get('header_text_film'),
                                     get_query_type('kw'),
                                     film_keyword,
                                     column_title.get('column_title_film'),
                                     numbered_rows[start:end])
            if end >= len(film_result):
                break
            # Спрашиваю у пользователя, продолжать ли:
            print(f'\t\033[0;38m Would you like to continue the list?\033[m')
            ask = input(f'\tEnter any key to continue or \033[0;32m"n"\033[m to stop: ')
            # ask = 'y'
            if ask.lower() == 'n':
                break
            # Переход к следующему "пакету" данных, те к следующим 10-ти:
            start += chunk_size
            end += chunk_size

    # return --- здесь НЕ нужен, тк функция НЕ выполняет вычисления или обработку данных, и НЕ ожидается
    # использовать её результат в дальнейшем. Функция просто выполняет действие, выводя на экран результат,
    # или изменяет данные, но не возвращает результат.
