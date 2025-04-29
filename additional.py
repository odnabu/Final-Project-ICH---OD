
# %%%%%%%%%______ ЧТЕНИЕ данных из БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# ___ Типы ПОИСКОВЫХ ЗАПРОСОВ:
#       - Film - по ключевому слову из названия фильма,
#       - Genre & Year - по жанру и по году,
#       - pq - popular_search (queries).

def get_query_type(key):
    query_type = {'kw': 'keyword', 'g_y': 'genre_year', 'g': 'genre', 'y': 'year',
                  'pq': 'popular_search'}
    return query_type.get(key)


# ___ Ключевое слово для поисковых запросов в таблице film БД sakila:
def ask_film_keyword():
    print(f'\n \033[32m▹\033[m To find a film by keyword in a title')
    while True:
        keyword = input(f'   ENTER the keyword for searching: ').lower()
        # keyword = 'oce'
        if keyword != '':
            return keyword
        else:
            print(f' \033[40;38m SORRY \033[m Please enter at least one symbol for the keyword: ')
