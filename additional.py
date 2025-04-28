
# %%%%%%%%%______ ЧТЕНИЕ данных из БД sakila ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


# ___ Типы ПОИСКОВЫХ ЗАПРОСОВ:
#       - Film - по ключевому слову из названия фильма,
#       - Genre - по жанру,
#       - Year - по году.
def get_query_type(key):
    query_type = {'kw': 'keyword', 'g_y': 'genre_year', 'g': 'genre', 'y': 'year',
                  'pq': 'popular_search'}
    return query_type.get(key)
# print(get_query_type('kw'))



# ___ Ключевое слово для поисковых запросов в таблице film БД sakila:
def ask_film_keyword():
    print(f'\nTo find a film by keyword in a title')
    while True:
        # keyword = input(f'ENTER the keyword for searching: ').lower()
        keyword = 'oce'
        if keyword != '':
            return keyword
        else:
            print('Please enter at least one symbol for the keyword.')

# film_keyword = str(ask_film_keyword())



