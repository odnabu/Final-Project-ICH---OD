
# +++++++++++++++++++++++++++++++++++
from prettytable import PrettyTable
# +++++++++++++++++++++++++++++++++++

# %%%%%%%%%______ Оформление таблицы в выводе результатов ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Текст в заголовке до search_type --> header_text
# Тип поискового запроса --> search_type /// search_type.
# Ключевое слово для поиска --> film_keyword
# Имена столбцов --> column_title. NB! кол-во элементов в списке имен должно быть таким же сколько и в списке data_in_col.
# Данные для вывода --> data_in_col.

def print_one_field_as_table(header_text, search_type, film_keyword, column_title, data_in_col):
    """
    Функция форматирования таблицы и печати содержимого.
    """
    x = PrettyTable()
    x.title = f'🔜 {header_text} {search_type} \033[35m\"{film_keyword}\" \033[m'       # 🔜🗄️»»⁜※▤⊟⋙⋙
    x.header = True
    # x.header_style = 'title'
    x.align = 'l'
    x.vertical_char = ' '
    x.horizontal_char = f'\033[35m—\033[m'
    x.junction_char = '\033[35m•\033[m'
    x.padding_width = 2
    x.field_names = column_title
    x.add_rows(data_in_col)
    print(x)


# Имена столбцов в выводе таблице:
column_title = {
    'column_title_film': ['N', 'Tile', 'Year', 'Duration'],
    'column_title_genre': ['N', 'Tile'],
    'column_title_year': ['from', 'to'],
    'column_title_popular': ['N', 'Type of search', 'Content of search']
}


# Текст в заголовке до search_type --> header_text
header_text = {
    'header_text_film': 'Films by',
    'header_text_categor': 'List of',
    'header_text_popul': 'The most',
    'header_text_max_min_year': 'Range for'
}
