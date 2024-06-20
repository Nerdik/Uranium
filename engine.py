
import pandas as pd


#-----------------------------------------------------------------------------------------------------------------------------
# Функции для связи с интерфейсом
#-----------------------------------------------------------------------------------------------------------------------------

'''
< Окно Загрузка файлов > Функция загружающая файлы в соответствии со спсиском - кнопка Загрузить файлы
'''
def load_files_engine(files_list):
    print(files_list)                     




'''
< Окно Настройка запросов > Функция подающая текстовый запрос на LLM - кнопка Запуск LLM
'''
def LLM_input_engine(LLM_input_text):
    print(f"Saved text: {LLM_input_text}")


def table_columns_engine():
    # DataFrame с данными столбцов итоговой таблицы - тут приведен для демонстрации работы
    columns = {
        'Наименование столбца итоговой таблицы': ['John', 'Jane', 'Mike', '']
        }
    columns_df = pd.DataFrame(columns)
    return columns_df


def update_table_columns_engine(columns_df, row, col, new_value):
    columns_df.iloc[row, col] = new_value
    print(columns_df)



'''
< Окно Контроль вывода > Функция пполучающая информацию из таблицы
'''

def control_table_columns_engine():
    # DataFrame с данными таблицы сгруппированных столбцов - тут приведен для демонстрации работы
   
    columns_settings = {
            'Группа': ['Столбец 1', '', '', 'Столбец 2', '', ''],
            'Excel1': [25, 30, 35, 25, 30, 35],
            'Excel2': [25, 30, 35, 25, 30, 35],
            'Excel3': [25, 30, 35, 25, 30, 35],
            'Объединение': ['да', '', '', 'да', '', '']
            }
    columns_settings_df = pd.DataFrame(columns_settings)
    return columns_settings_df

def update_table_columns_engine(columns_df):
    # columns_df.iloc[row, col] = new_value
    print(columns_df)




'''
< Окно Выгрузка результата > Функция создающая и сохраняющая файл Excel - кнопка Создать файл Excel
'''
def table_file_preview_engine():
    # DataFrame с данными таблицы сгруппированных столбцов - тут приведен для демонстрации работы
    table_preview = {
        'Столбец 1': 
        ['John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike'],
        'Столбец 2': 
        [25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35],
        'Столбец 3': 
        ['New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris'],
        'Столбец 4': 
        ['John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike'],
        'Столбец 5': 
        [25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35],
        'Столбец 6': 
        ['New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris'],
        'Столбец 7': 
        ['John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike'],
        'Столбец 8': 
        [25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35],
        'Столбец 9': 
        ['New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris'],
        'Столбец 10': 
        ['John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike', 'John', 'Jane', 'Mike'],
        'Столбец 11': 
        [25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35, 25, 30, 35],
        'Столбец 12': 
        ['New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris', 'New York', 'London', 'Paris']
        }
    table_preview_df = pd.DataFrame(table_preview)
    return table_preview_df

def create_file_engine(table_preview_df):
    print(table_preview_df)