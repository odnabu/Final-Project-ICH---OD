# %%%%%%%%%______ ЧТЕНИЕ данных из БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# +++++++++++++++++++++++++++++++++++++++++++++++
# ___ Вызовы из моих файлов: ___________________
from queries import queries
from decor import (print_one_field_as_table, column_title)
from film_by_keyword import get_query_type
# +++++++++++++++++++++++++++++++++++++++++++++++

l = 60

# --------------------------------------------------------------------- #
#       3. Печать самых поисковых запросов по частоте использования     #
# --------------------------------------------------------------------- #

def get_popular_search_query(cursor):
    try:
        results_amount = int(input('Enter the amount of results: '))
        cursor.execute(queries.get('popular_search_query'), (results_amount,))
        popular_search = cursor.fetchall()
        # Извлечение данных из результата запроса:
        numbered_rows = [(index, *row) for index, row in enumerate(popular_search, start=1)]
        print(
            f'\n\t\033[33m {results_amount}\033[m most popular search queries: ')
        print_one_field_as_table(get_query_type('pq'), column_title.get('column_title_popular'), numbered_rows)
    except ValueError:
        notice = f' \033[40;38m SORRY \033[m'
        print(f'{'':▿<{l}}\n{notice:15}'
              f' You should enter the NUMBER. Try it again.'
              f'\n{'':▵<{l}}')

