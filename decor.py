
# +++++++++++++++++++++++++++++++++++
from prettytable import PrettyTable
# +++++++++++++++++++++++++++++++++++

# %%%%%%%%%______ Оформление таблицы в выводе результатов ______%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# c_t --> chosen_table, col_t --> column_title, d_c --> data_in_col
def print_one_field_as_table(c_t, col_t, d_c):
    x = PrettyTable()
    x.title = f'🔜 Data by query: \033[35m\"{c_t}\" \033[m'       # 🔜🗄️»»⁜※▤⊟⋙⋙
    x.header = True
    # x.header_style = 'title'
    x.align = 'l'
    x.vertical_char = ' '
    x.horizontal_char = f'\033[35m—\033[m'
    x.junction_char = '\033[35m•\033[m'
    x.padding_width = 2
    x.field_names = col_t
    x.add_rows(d_c)
    print(x)

# Имена столбцов в выводе таблице:
column_title = ['N', 'Tile', 'Year', 'Duration']     # , 'DESCRIPTION'

