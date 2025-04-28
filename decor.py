
# +++++++++++++++++++++++++++++++++++
from prettytable import PrettyTable
# +++++++++++++++++++++++++++++++++++

# %%%%%%%%%______ Оформление таблицы в выводе результатов ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Таблица, из которой берутся данные --> chosen_table.
# Имена столбцов --> column_title. NB! кол-во элементов в списке имен должно быть таким же сколько и в списке data_in_col.
# Данные для вывода --> data_in_col.
def print_one_field_as_table(chosen_table, column_title, data_in_col):
    x = PrettyTable()
    x.title = f'🔜 Films by: \033[35m\"{chosen_table}\" \033[m'       # 🔜🗄️»»⁜※▤⊟⋙⋙
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
column_title_film = ['N', 'Tile', 'Year', 'Duration']     # , 'DESCRIPTION'
column_title_genre = ['N', 'Tile']
column_title_year = ['from', 'to']
