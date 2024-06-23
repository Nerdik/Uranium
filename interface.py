import sys
import os
import pandas as pd
from pathlib import Path
from PyQt6.QtGui import QPixmap, QColor 
from PyQt6.QtCore import (
    QSize, Qt, QBasicTimer, QCoreApplication,
    QThread, pyqtSignal
)
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QWidget,
    QMainWindow, QLabel, QGridLayout, QPushButton,
    QFileDialog, QTextEdit, QListWidget, QListWidgetItem,
    QTableView, QTableWidgetItem, QTableWidget,
    QStackedLayout, QHBoxLayout, QVBoxLayout,
    QLineEdit, QSpacerItem, QSizePolicy, QProgressBar,
    QDialog
)
from Get_dictionary_Michael import CreateDF_FromGlobalDict
from engine import (
    load_files_engine,
    LLM_input_engine,
    start_LLM_engine,
    table_columns_engine,
    update_table_columns_engine,
    control_table_columns_engine,
    table_file_preview_engine,
    create_file_engine
)

# from Get_dictionary_Michael import Get_DF_from_Dictionary, Get_Small_Dictionary_from_Excel, select_excel_files, Get_ALL_Dictionary_from_Excel
# from Multilingual_e5_Vlad import get_words_from_multilingual_e5_base
# from Multilingual_Alex import get_words_from_multilingual_bert
# import pandas as pd
# import copy
# import os
from Test import Get_global_dict
from Ask_Gigachat import Get_Answer_LLM

#-----------------------------------------------------------------------------------------------------------------------------
# Основной код интерфейса
#-----------------------------------------------------------------------------------------------------------------------------

'''
Глобальные переменнные
'''

# Глобальный словарь для таблиц
final_global_dict = {}

# Список групп столбцов
columns_list =[]

# Список файлов
files_list = []

# Количество выводимых вариантов столбцов
quantity = 3


# Инициализация df
global df
df = pd.DataFrame()
    

# class ProgressBarWidget(QWidget):
#     '''
#     Класс прогресс-бара 
#     '''
#     def __init__(self):
#         super().__init__()
#         self.initUI()

#     def initUI(self):
#         self.layout = QVBoxLayout(self)
#         self.progress_bar = QProgressBar(self)
#         self.progress_bar.setMinimum(0)
#         self.progress_bar.setMaximum(100)
#         self.layout.addWidget(self.progress_bar)

#     def set_progress(self, value):
#         self.progress_bar.setValue(value)


# class WorkerThread(QThread):
#     '''
#     Класс рабочего потока для прогресс-бара
#     '''
#     progress_changed = pyqtSignal(int)
    
#     def __init__(self, data, parent=None):
#         super().__init__(parent)
#         self.data = data
    
#     def run(self):
#         total_steps = len(self.data)
#         for i, item in enumerate(self.data):
#             # Ваш длительный процесс здесь
#             self.do_work(item)
#             progress = int((i + 1) / total_steps * 100)
#             self.progress_changed.emit(progress)
    
#     def do_work(self, item):
#         # Имитация работы (заменить на реальную функцию)
#         QThread.sleep(1)  # Удалить или заменить на реальный процесс

class LoadFileDialog(QDialog):
    '''
    Класс окна диалога с сообщением, что загрузка файлов завершена
    '''
    def __init__(self):
        super(LoadFileDialog, self).__init__()

        self.setWindowTitle("Загрузка файлов")
        self.setFixedSize(400, 150)

        # Основной макет
        self.layout = QGridLayout(self)

        cell_widget_1 = QWidget()
        cell_widget_1.setStyleSheet("background-color: #32363F;")

        # Виджеты 
        self.label = QLabel("Загрузка файлов завершена")

        # Кнопка ок
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.cancel)

        # Устанавливаем фиксированные размеры для виджетов   
        self.ok_button.setMinimumSize(150, 50)
        self.ok_button.setMaximumSize(150, 50)

        # Добавление виджетов в макет
        self.layout.addWidget(self.label, 0, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.ok_button, 1, 0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.canceled = False

        # Устанавливаем общий цвет фона окна
        self.setStyleSheet("""
            QDialog {
                background-color: #32363F; /* Устанавливаем цвет фона окна */
            }
            QPushButton {
                background-color: #32363F;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #252932;
                color: #00B5FF;
            }
            QLabel {
                color: #f0f0f0;
                font-size: 12px;
            }
        """)

    def cancel(self):
        self.canceled = True
        self.close()

    def is_canceled(self):
        return self.canceled


class HomeLayout(QWidget):
    '''
    Класс вкладки меню Home 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 0, 40, 0)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 0, 40, 0)
        self.grid_layout2 = QGridLayout()
        self.grid_layout2.setContentsMargins(0, 0, 0, 0)

        image_path_1 = 'images/gazprom_logo.jpg'
        image_path_2 = 'images/fkn_logo.jpg'
        image_path_3 = 'images/home.jpg'

        # Создаем виджеты
        self.label1 = QLabel("Home page")
        self.image_label_1 = QLabel()
        self.image_label_2 = QLabel()
        self.image_label_3 = QLabel()
        self.pixmap_1 = QPixmap(image_path_1)
        self.image_label_1.setPixmap(self.pixmap_1)
        self.pixmap_2 = QPixmap(image_path_2)
        self.image_label_2.setPixmap(self.pixmap_2)
        self.pixmap_3 = QPixmap(image_path_3)
        self.image_label_3.setPixmap(self.pixmap_3)


        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.image_label_1.setScaledContents(True)
        self.image_label_1.setFixedSize(275, 150)
        self.image_label_2.setScaledContents(True)
        self.image_label_2.setFixedSize(275, 150)

        # Устанавливаем цвет фона виджета
        self.color_widget_1 = QWidget()
        self.color_widget_1.setStyleSheet("background-color: #ffffff;")

        self.color_widget_2 = QWidget()
        self.color_widget_2.setStyleSheet("background-color: #000000;")
        
        # Добавляем виджеты в сетку
        # self.page_layout.setSpacing(20)
        # self.page_layout.addWidget(self.label1, 0, 0)
        # self.page_layout.setSpacing(20)

        self.page_layout.addLayout(self.grid_layout, 1, 0)
        self.grid_layout.addWidget(self.color_widget_1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.image_label_1, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.grid_layout.addWidget(self.image_label_2, 0, 1, alignment=Qt.AlignmentFlag.AlignRight)
        self.page_layout.addLayout(self.grid_layout2, 2, 0)
        self.grid_layout2.addWidget(self.color_widget_2, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout2.addWidget(self.image_label_3, 0, 0, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)



        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)

        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget_1, 1, 0)
        self.page_layout.addWidget(self.color_widget_2, 2, 0)


class UploadLayout(QWidget):
    '''
    Класс вкладки меню Загрузка файлов 
    '''
    def __init__(self):
        super().__init__()
        
        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 40, 40, 40)
       
        # Создаем видже
        self.label1 = QLabel("Загрузка файлов")
        self.file_list_widget = QListWidget()
        self.button1 = QPushButton("Добавить файлы")
        self.button2 = QPushButton("Удалить файл")
        self.button3 = QPushButton("Загрузить файлы в систему")
        self.label2 = QLabel("Выбранные файлы: ")

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем минимальные размеры для кнопок   
        self.button1.setMinimumSize(200, 50)
        self.button2.setMinimumSize(200, 50)
        self.button3.setMinimumSize(200, 50)
        self.file_list_widget.setMinimumSize(200, 400)
        
        # Устанавливаем цвет фона виджета
        self.color_widget = QWidget()
        self.color_widget.setStyleSheet("background-color: #32363F;")       
        
        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label1, 0, 0)
        
        self.page_layout.addLayout(self.grid_layout, 1, 0)
        self.grid_layout.addWidget(self.color_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.label2, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.file_list_widget, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.button1, 2, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.button2, 2, 1, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.page_layout.addWidget(self.button3, 2, 0)

        self.page_layout.addItem(spacer, 2, 0)      

        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 1)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 0)

        # Подключаем сигнал нажатия на кнопки
        self.button1.clicked.connect(self.add_file)
        self.button2.clicked.connect(self.remove_file)
        self.button3.clicked.connect(self.load_file)

        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget, 1, 0)

        # Список загружаемых файлов
        


    def add_file(self):
        # Открываем диалоговое окно для выбора файла
        global files_list
        file_names, _ = QFileDialog.getOpenFileNames(self, "Открыть файлы", "", "Все файлы (*);;Текстовые файлы (*.txt)")
        if file_names:
            for name in file_names:
                if name not in files_list:
                    files_list.append(rf'{Path(name)}')
                    self.file_list_widget.addItem(name)                       


    def remove_file(self):
        # Удаляем выбранный файл из списка
        global files_list
        selected_items = self.file_list_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            path = item.text().replace('/', '\\')
            files_list.remove(path)
            self.file_list_widget.takeItem(self.file_list_widget.row(item))                         
    

    def load_file(self):
        # Загружаем файлы в engine.py
        global files_list
        load_files_engine(files_list)           # TODO Перетащить сюда функцию
        self.dialog = LoadFileDialog()
        self.dialog.show()


class SettingsLayout(QWidget):
    '''
    Класс вкладки меню Настройка запроса 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout_1 = QGridLayout()
        self.grid_layout_1.setContentsMargins(40, 40, 40, 40)
        self.grid_layout_2 = QGridLayout()
        self.grid_layout_2.setContentsMargins(40, 40, 40, 40)

        # Создаем виджеты
        self.label3 = QLabel("Запрос с применением LLM")
        self.label4 = QLabel("Введите текстовый запрос")
        self.text_input = QTextEdit()
        self.button1 = QPushButton("Запуск LLM")   
               
        self.label1 = QLabel("Настройка запроса")
        self.label2 = QLabel("Таблица контроля выбранных столбцов")
        self.check_table = QTableWidget()
        self.button2 = QPushButton("Добавить строку")
        self.button3 = QPushButton("Удалить строку")  

        # global columns_list
        # columns_list, self.columns_df = self.Get_Answer_LLM_interface(self.text_input.toPlainText())
        # self.columns_df = self.Get_Answer_LLM_interface(self.text_input.toPlainText())                     # TODO <- Функция загрузки из engine.py
        # self.check_table.setRowCount(len(self.columns_df))
        # self.check_table.setColumnCount(len(self.columns_df.columns))
        # self.check_table.setHorizontalHeaderLabels(self.columns_df.columns)

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.button1.setMinimumSize(200, 50)
        self.text_input.setMinimumSize(200, 50)
        self.check_table.setMinimumSize(200, 200)
        self.button2.setMinimumSize(200, 50)
        self.button3.setMinimumSize(450, 50)

        # Устанавливаем цвет фона виджета
        self.color_widget_1 = QWidget()
        self.color_widget_1.setStyleSheet("background-color: #32363F;")
        self.color_widget_2 = QWidget()
        self.color_widget_2.setStyleSheet("background-color: #32363F;")   

        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label3, 0, 0, 1, 2)

        self.page_layout.addLayout(self.grid_layout_2, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.color_widget_2, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.label4, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.text_input, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_2.addWidget(self.button1, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)       
    
        self.page_layout.addWidget(self.label1, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)

        self.page_layout.addLayout(self.grid_layout_1, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_1.addWidget(self.color_widget_1, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_1.addWidget(self.label2, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_1.addWidget(self.check_table, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout_1.addWidget(self.button2, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)  
        self.grid_layout_1.addWidget(self.button3, 3, 1, alignment=Qt.AlignmentFlag.AlignTop)  

        self.page_layout.addItem(spacer, 4, 0)

        # Устанавливаем stretch-факторы
        self.page_layout.setRowStretch(0, 0)
        self.grid_layout_2.setRowStretch(0, 0)
        self.grid_layout_2.setRowStretch(1, 0)
        self.grid_layout_2.setRowStretch(2, 0)
        self.grid_layout_2.setRowStretch(3, 1)
        self.page_layout.setRowStretch(1, 0)
        self.grid_layout_1.setRowStretch(0, 0)
        self.grid_layout_1.setRowStretch(1, 0)
        self.grid_layout_1.setRowStretch(2, 0)
        self.grid_layout_1.setRowStretch(3, 1)
        self.grid_layout_1.setColumnStretch(0, 1)
        self.grid_layout_2.setColumnStretch(0, 1)

        # Создаем вспомогательный виджет для второго фона
        self.page_layout.addWidget(self.color_widget_2, 1, 0)        
        self.page_layout.addWidget(self.color_widget_1, 3, 0)
              

        # # Заполнение таблицы данными из DataFrame 
        # for row in range(len(self.columns_df)):
        #     for col in range(len(self.columns_df.columns)):
        #         self.check_table.setItem(row, col, QTableWidgetItem(str(self.columns_df.iloc[row, col])))

        # # Установить ширину столбцов и высоту строк
        # for col in range(len(self.columns_df.columns)):
        #     self.check_table.setColumnWidth(col, 730)

        # Подключение сигнала изменения ячейки к обработчику
        self.check_table.cellChanged.connect(self.update_data)

        # Подключаем сигнал нажатия на кнопки запуска LLM
        self.button1.pressed.connect(self.update_table_LLM_input)
        self.button2.pressed.connect(self.add_row_table)
        self.button3.pressed.connect(self.delete_raw_table)

        # Задаем пустое начальное значение ввода для LLM
        self.LLM_input_text = ''

    def update_table_LLM_input(self):
        global columns_list
        columns_list, dataframe = self.Get_Answer_LLM_interface(self.text_input.toPlainText())
        # dict1 = {'Наименование столбца итоговой таблицы': ['Скважина', 'Газ', 'Добыча']}
        # dataframe = pd.DataFrame(dict1)
        # columns_list = ['Скважина', 'Газ', 'Добыча']
        self.check_table.clearContents()
        self.check_table.setRowCount(len(dataframe))
        self.check_table.setColumnCount(len(dataframe.columns))
        self.check_table.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(len(dataframe)):
            for col in range(len(dataframe.columns)):
                self.check_table.setItem(row, col, QTableWidgetItem(str(dataframe.iloc[row, col])))
        
        for col in range(len(dataframe.columns)):
            self.check_table.setColumnWidth(col, 730)

    def add_row_table(self):
        columns_list.append('')
        dict1 = {}                                                                  # TODO <- Функция загрузки из engine.py
        dict1['Наименование столбца итоговой таблицы'] = columns_list               # TODO <- Функция загрузки из engine.py
        dataframe = pd.DataFrame(dict1)                                             # TODO <- Функция загрузки из engine.py
        self.check_table.clearContents()
        self.check_table.setRowCount(len(dataframe))
        self.check_table.setColumnCount(len(dataframe.columns))
        self.check_table.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(len(dataframe)):
            for col in range(len(dataframe.columns)):
                self.check_table.setItem(row, col, QTableWidgetItem(str(dataframe.iloc[row, col])))
        
        for col in range(len(dataframe.columns)):
            self.check_table.setColumnWidth(col, 730)

            
    def delete_raw_table(self):
        dict1 = {}                                                                  # TODO <- Функция загрузки из engine.py
        columns_list.pop()
        dict1['Наименование столбца итоговой таблицы'] = columns_list               # TODO <- Функция загрузки из engine.py
        dataframe = pd.DataFrame(dict1)                                                    # TODO <- Функция загрузки из engine.py
        self.check_table.clearContents()
        self.check_table.setRowCount(len(dataframe))
        self.check_table.setColumnCount(len(dataframe.columns))
        self.check_table.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(len(dataframe)):
            for col in range(len(dataframe.columns)):
                self.check_table.setItem(row, col, QTableWidgetItem(str(dataframe.iloc[row, col])))
        
        for col in range(len(dataframe.columns)):
            self.check_table.setColumnWidth(col, 730)


    def update_data(self, row, col):
        # Обновление DataFrame при изменении данных в таблице
        global columns_list
        new_value = self.check_table.item(row, col).text()
        columns_list[row] = new_value
        print(columns_list)      # TODO <- Функция загрузки из engine.py


    # def LLM_input(self):
    #     self.LLM_input_text = self.text_input.toPlainText()
    #     LLM_input_engine(self.LLM_input_text)                    # TODO <- Функция загрузки из engine.py

    def Get_Answer_LLM_interface(self, request_text):
        #промт в гигачат
        request_promt = f'Из следующего предложения вычлени заголовки для таблицы в виде списка: {request_text}'
        #получаем ответ от гигачата
        request = Get_Answer_LLM(request_text,request_promt)
        #Постобработка ответа гигачата
        request = request.splitlines()
        # Удаление номеров элементов
        request = [элемент.split('.', 1)[-1].strip() for элемент in request if элемент.strip()]
        request = [item for item in request if ("Заголовки" not in item and "заголовки" not in item)]
        request_dict = {'Наименование групп столбцов': request}
        request_df = pd.DataFrame(request_dict)     
        return request, request_df
     

class ControlLayout(QWidget):
    '''
    Класс вкладки меню Контроль вывода 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 40, 40, 40)
        # self.progress_bar_widget = ProgressBarWidget()

        # Создаем виджеты
        self.label1 = QLabel("Контроль вывода")
        self.label2 = QLabel("Таблица контроля выбранных столбцов")
        self.check_table = QTableWidget()
        self.columns_settings_df = control_table_columns_engine()                        # TODO <- Функция загрузки из engine.py
        self.progress_button = QPushButton("Запуск формирования таблицы с LLM")
        self.button1 = QPushButton("Оставить только выбранные столбцы")
        self.button2 = QPushButton("Вернуть начальную подборку")
        # self.button3 = QPushButton("Сформировать итоговую таблицу")
        
        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.check_table.setMinimumSize(200, 400)
        self.button1.setMinimumSize(200, 50)
        self.button2.setMinimumSize(200, 50)
        # self.button3.setMinimumSize(200, 50)
        self.progress_button.setMinimumSize(200, 50)

        # Устанавливаем цвет фона виджета
        self.color_widget = QWidget()
        self.color_widget.setStyleSheet("background-color: #32363F;")

        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label1, 0, 0)

        self.page_layout.addLayout(self.grid_layout, 1, 0)
        self.grid_layout.addWidget(self.color_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.label2, 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.check_table, 1, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.progress_button, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        # self.grid_layout.addWidget(self.progress_bar_widget, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.button1, 4, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.button2, 4, 1, alignment=Qt.AlignmentFlag.AlignTop)

        # self.page_layout.addWidget(self.button3, 2, 0)     
        
        self.page_layout.addItem(spacer, 2, 0)

        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 0)
        self.grid_layout.setRowStretch(3, 0)
        self.grid_layout.setRowStretch(4, 1)
        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 1)
       
        # Создание первичной backup версии таблицы
        # backup_global_dict = Get_global_dict(SettingsLayout().columns_df, 0, 0)
        
        # Подключаем сигнал нажатия на кнопки запуска LLM
        global backup_table
        self.button1.pressed.connect(lambda: self.update_colors(color_table))
        self.button2.pressed.connect(lambda: self.update_table(backup_table))
        # self.button3.pressed.connect(lambda: self.preview_formation(final_global_dict))

        # Подключаем сигнал нажатия на кнопку запуска формирования таблицы
        global columns_list
        global files_list
        global quantity
        self.progress_button.pressed.connect(lambda: self.start_formation(columns_list, quantity, files_list))
        
        # Подключение сигнала изменения ячейки к обработчику
        self.check_table.cellClicked.connect(self.update_data)
        
        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget, 1, 0)


    def start_formation(self, list, quantity, files_list):
         
        global final_global_dict
        print('Список запросов: ',list)
        final_global_dict = Get_global_dict(list, quantity, files_list)
        # for key in final_global_dict.keys():
        #     print('Малый словарь после мульти:',final_global_dict[key][0])
        global color_table
        color_table = CreateDF_FromGlobalDict(final_global_dict, quantity)
        global backup_table
        backup_table = color_table
        self.update_table(color_table)
    
        # self.update_table(dataframe)
        # data = list(range(100))  # Замените на реальные данные для обработки
        # self.worker_thread = WorkerThread(data)
        # self.worker_thread.progress_changed.connect(self.progress_bar_widget.set_progress)
        # self.worker_thread.start()



    def update_table(self, dataframe):
        # Заполнение таблицы данными из DataFrame
        self.check_table.clearContents()
        self.check_table.setRowCount(len(dataframe))
        self.check_table.setColumnCount(len(dataframe.columns))
        self.check_table.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(len(dataframe)):
            for col in range(len(dataframe.columns)):
                self.update_item(row, col, dataframe)
                self.check_table.item(row, col).setBackground(QColor(255, 255, 255))


    def update_colors(self, dataframe):
        # Функция обновления таблицы с учетом отмеченных ячеек
        updated_dict = {col: [] for col in dataframe.columns}
        for col in range(len(dataframe.columns)):
            for row in range(len(dataframe)):
                item = self.check_table.item(row, col)
                if col == 0:
                    if item is not None and item.text().strip() != '':
                        updated_dict[dataframe.columns[col]].append(item.text().strip())          
                elif self.check_table.item(row, col).background().color().red() == 0:
                    updated_dict[dataframe.columns[col]].append(item.text().strip()) 
        global updated_df          
        updated_df = pd.DataFrame(updated_dict)
        self.update_table(updated_df)


    # def preview_formation(self, dict):
        # global updated_df
        # minus_dict = self.GlobalDFS_Minus_df(dict, updated_df)
        # self.Get_dataframe_preview(minus_dict)
        # ResultLayout().update_preview_table(df)
        


        
    
    
    def update_item(self, row, col, dataframe):
        # Функция обновления отображения данных ячейки в таблице
        self.check_table.setItem(row, col, QTableWidgetItem(str(dataframe.iloc[row, col])))
    
    
    def update_data(self, row, col):
        # Функция обновления данных ячейки 
        if col != 0:
            cell = self.check_table.item(row, col).background().color().red()
            match cell:
                case 255:
                    self.check_table.item(row, col).setBackground(QColor(0, 255, 0))
                case 0:
                    self.check_table.item(row, col).setBackground(QColor(255, 255, 255))


class ResultLayout(QWidget):
    '''
    Класс вкладки меню Выгрузка результата 
    '''
    def __init__(self):
        super().__init__()

        # Объявляем макеты
        self.page_layout = QGridLayout(self)
        self.page_layout.setContentsMargins(40, 40, 40, 40)
        self.grid_layout = QGridLayout()
        self.grid_layout.setContentsMargins(40, 40, 40, 40)
        button_layout = QHBoxLayout()

        # Создаем виджеты
        self.label1 = QLabel("Выгрузка результата")
        self.label2 = QLabel("Предварительный просмотр итоговой таблицы")
        self.check_table = QTableWidget()
        # self.table_preview_df = table_file_preview_engine()                        # TODO <- Функция загрузки из engine.py
        
        self.button1 = QPushButton("Создать Excel последовательно")
        self.button2 = QPushButton("Создать Excel параллельно")

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        # Устанавливаем фиксированные размеры для виджетов   
        self.check_table.setMinimumSize(200, 500)
        self.button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Устанавливаем цвет фона виджета
        self.color_widget = QWidget()
        self.color_widget.setStyleSheet("background-color: #32363F;")

        # Добавляем виджеты в сетку
        self.page_layout.setSpacing(20)
        self.page_layout.addWidget(self.label1)
        self.page_layout.setSpacing(20)

        self.page_layout.addLayout(self.grid_layout, 1, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.color_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        self.grid_layout.addWidget(self.label2, 1, 0, 1, 2)
        self.grid_layout.addWidget(self.check_table, 2, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignTop)
        # self.grid_layout.addWidget(self.button1, 3, 0, alignment=Qt.AlignmentFlag.AlignTop)
        # self.grid_layout.addWidget(self.button2, 3, 1, alignment=Qt.AlignmentFlag.AlignTop)

        # Создаем горизонтальный макет для кнопок
        self.grid_layout.addLayout(button_layout, 3, 0, 1, 2)
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)

        # Устанавливаем политику размера для кнопок
        self.button1.setMinimumSize(200, 50)
        self.button2.setMinimumSize(200, 50)
        self.button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.page_layout.addItem(spacer, 2, 0)

        # Устанавливаем stretch-факторы
        self.grid_layout.setRowStretch(0, 0)
        self.grid_layout.setRowStretch(1, 0)
        self.grid_layout.setRowStretch(2, 0)
        self.grid_layout.setRowStretch(3, 1)
        self.grid_layout.setColumnStretch(0, 0)
        self.grid_layout.setColumnStretch(1, 1)     
        
        # Создаем вспомогательный виджет для второго фона в QVBoxLayout
        self.page_layout.addWidget(self.color_widget, 1, 0)

        # Подключаем сигнал нажатия на кнопки
        global df
        self.button1.clicked.connect(lambda: self.Get_Excel_sequent(df, final_global_dict))
        self.button2.clicked.connect(lambda: self.Get_Excel_parallel(df, final_global_dict))

    def update_preview_table(self, dataframe):
        # Заполнение таблицы данными из DataFrame
        self.check_table.clearContents()
        self.check_table.setRowCount(len(dataframe))
        self.check_table.setColumnCount(len(dataframe.columns))
        self.check_table.setHorizontalHeaderLabels(dataframe.columns)

        for row in range(len(dataframe)):
            for col in range(len(dataframe.columns)):
                self.update_item(row, col, dataframe)
                self.check_table.item(row, col).setBackground(QColor(255, 255, 255))


    def update_item(self, row, col, dataframe):
        # Функция обновления отображения данных ячейки в таблице
        self.check_table.setItem(row, col, QTableWidgetItem(str(dataframe.iloc[row, col])))


    def Get_dataframe_preview(self, global_dict):
        # Создание DataFrame для экспорта в Excel
        global df
        df = pd.DataFrame(columns=global_dict.keys())
        # Добавление данных в DataFrame
        i=-1
        for key in global_dict:
            i=i+1
            values=[]
            #Извлекаем большие словари для каждого ключа
            s_big=global_dict[key][0]
            #Заходим внутрь, тут еще один словарь, где ключи это заголовки
            for excel_key in s_big:
                s_excel_big = s_big[excel_key]
                #Заходим в последнюю матрешку,в словарь, где ключи заголовки
                for zagolovok_excel_key in s_excel_big:
                    values.extend(s_excel_big[zagolovok_excel_key].values)
            # Проверяем, нужно ли изменить размер DataFrame
            num_rows = len(df)
            num_values = len(values)
            if num_values > num_rows:
                # Увеличиваем DataFrame до нужного размера
                df = df.reindex(range(num_values))
            elif num_values < num_rows:
                # Обрезаем DataFrame до нужного размера
                df = df.iloc[:num_values]
            df.iloc[:, i] = values
        return df


    def GlobalDFS_Minus_df(self, dfs_global, df):
    # Получение списка значений первого столбца датафрейма
        valid_keys = df.iloc[:, 0].tolist()
        
        # Очистка словаря dfs_global
        cleaned_dfs_global = {}
        for key, small_list in dfs_global.items():
            if key in valid_keys:
                # Копируем первый элемент списка без изменений
                cleaned_small_list = [small_list[0]]
                if len(small_list) > 1:
                    small_dict = small_list[1]
                    cleaned_small_dict = {}
                    for sub_key, sub_values in small_dict.items():
                        if sub_key in df.columns:
                            cleaned_sub_values = [val for val in sub_values if val in df[sub_key].values]
                            cleaned_small_dict[sub_key] = cleaned_sub_values
                    cleaned_small_list.append(cleaned_small_dict)
                cleaned_dfs_global[key] = cleaned_small_list
        for key in cleaned_dfs_global.keys():                               # Заменил .items() на .keys()
            cleaned_dfs_global[key][0]= self.BigDfs_Minus_Smalldfs(cleaned_dfs_global[key][0],cleaned_dfs_global[key][1])
        # Вывод результата
        print('Очищенный ',cleaned_dfs_global)
        return cleaned_dfs_global

    def BigDfs_Minus_Smalldfs(self, s_big,s_small):
        #Вычитание из большого словаря маленького
        # Получаем путь к файлу и лист
        file_path = list(s_small.keys())[0]
        # Получаем список допустимых столбцов из первого словаря
        valid_columns = s_small[file_path]
        # Отфильтровываем столбцы второго словаря
        filtered_data = {key: value for key, value in s_big[file_path].items() if key in valid_columns}

        # Обновляем второй словарь
        filtered_dict2 = {file_path: filtered_data}

        # Печатаем результат
        print('Отформатированный список:',filtered_dict2)
        return filtered_dict2
        
        
    def Get_Excel_sequent(self, df, dict):
        global updated_df
        minus_dict = self.GlobalDFS_Minus_df(dict, updated_df)
        df = self.Get_dataframe_preview(minus_dict)
        self.update_preview_table(df)
        # Сохранение DataFrame в Excel
        if os.path.exists('output.xlsx'):
            os.remove('output.xlsx')
            print(f"Файл {'output.xlsx'} успешно удален.")
        else:
            print(f"Файл {'output.xlsx'} не существует.")
        df.to_excel('output.xlsx', index=False)

    
    #Функция для создания DataFrame
    def create_dataframe_from_dfs_global(self,dfs_global):
        print('На обработку подался такой глобальный словарь',dfs_global)
        data = {}
        for outer_key, (inner_dict, _) in dfs_global.items():
            if inner_dict is not None:
                for inner_key, value_dict in inner_dict.items():
                    # Предполагается, что в value_dict всего один ключ, поэтому извлекаем первую (и единственную) серию
                    series = next(iter(value_dict.values()))
                    combined_key = f"{outer_key}+{inner_key}"
                    data[combined_key] = series
        print('Возвращается вот такой df: ',pd.DataFrame(data))
        return pd.DataFrame(data)

    def Get_Excel_parallel(self, df, dict):
        global updated_df
        print('До обработки был такой словарь ',dict)
        print('Вычитается такой df: ',updated_df)
        minus_dict = self.GlobalDFS_Minus_df(dict, updated_df)
        df = self.create_dataframe_from_dfs_global(minus_dict)
        self.update_preview_table(df)
        # Сохранение DataFrame в Excel
        if os.path.exists('output.xlsx'):
            os.remove('output.xlsx')
            print(f"Файл {'output.xlsx'} успешно удален.")
        else:
            print(f"Файл {'output.xlsx'} не существует.")
        df.to_excel('output.xlsx', index=False)


class MainWindow(QMainWindow):
    '''
    Класс главного окна
    '''
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Uranium table unifier")

        # Устанавливаем начальный размер окна
        self.resize(1300, 700)

        image_path = 'images/logo_uranium.jpg'

        widget = QWidget()
        self.setCentralWidget(widget)

        main_layout = QGridLayout(widget)
        main_layout.setContentsMargins(10, 0, 0, 0)
        menu_layout = QVBoxLayout()
        self.stack_layout = QStackedLayout()

        # Создаем виджеты
        self.image_label = QLabel()
        pixmap = QPixmap(image_path)
        self.image_label.setPixmap(pixmap)

        self.button0 = QPushButton("Главная")
        self.button1 = QPushButton("Загрузка файлов")
        self.button2 = QPushButton("Настройка запроса")
        self.button3 = QPushButton("Контроль вывода")
        self.button4 = QPushButton("Выгрузка результата")
        self.button_close = QPushButton("Выход")          

        # Устанавливаем фиксированные размеры для виджетов    
        self.button0.setMinimumSize(230, 50)
        self.button1.setMinimumSize(230, 50)
        self.button2.setMinimumSize(230, 50)
        self.button3.setMinimumSize(230, 50)
        self.button4.setMinimumSize(230, 50)
        self.button_close.setMinimumSize(200, 50)

        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(150, 150)

        # Устанавливаем разные цвета фона для разных ячеек
        cell_widget_1 = QWidget()
        cell_widget_1.setStyleSheet("background-color: #32363F;")

        cell_widget_2 = QWidget()
        cell_widget_2.setStyleSheet('background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #252932, stop:1 #2A2D34);')

        main_layout.addLayout(menu_layout, 0, 0, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addLayout(self.stack_layout, 0, 1, alignment=Qt.AlignmentFlag.AlignTop)
        main_layout.addWidget(cell_widget_1, 0, 0)
        main_layout.addWidget(cell_widget_2, 0, 1)

        # Добавляем виджеты в сетку
        menu_layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter) 
        menu_layout.addWidget(self.button0)
        menu_layout.addWidget(self.button1)
        menu_layout.addWidget(self.button2)
        menu_layout.addWidget(self.button3)
        menu_layout.addWidget(self.button4)
        menu_layout.addStretch()
        menu_layout.addWidget(self.button_close)
        menu_layout.addSpacing(20)   
                
        # Создаем экземпляры слоев и добавляем их в QStackedLayout
        self.home_layout = HomeLayout()
        self.stack_layout.addWidget(self.home_layout)
        
        self.start_layout = UploadLayout()
        self.stack_layout.addWidget(self.start_layout)

        self.settings_layout = SettingsLayout()
        self.stack_layout.addWidget(self.settings_layout)

        self.control_layout = ControlLayout()
        self.stack_layout.addWidget(self.control_layout)

        self.result_layout = ResultLayout()
        self.stack_layout.addWidget(self.result_layout)

        # Подключаем сигнал нажатия на кнопки
        self.button0.pressed.connect(lambda: self.activate_tab(0))
        self.button1.pressed.connect(lambda: self.activate_tab(1))
        self.button2.pressed.connect(lambda: self.activate_tab(2))
        self.button3.pressed.connect(lambda: self.activate_tab(3))
        self.button4.pressed.connect(lambda: self.activate_tab(4))
        self.button_close.pressed.connect(self.close)

        # Устанавливаем общий цвет фона окна
        self.setStyleSheet("""
            QMainWindow {
                background-color: #32363F; /* Устанавливаем цвет фона окна */
            }
            QPushButton {
                background-color: #32363F;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #252932;
                color: #00B5FF;
            }
            QLabel {
                color: #f0f0f0;
                font-size: 12px;
            }
            QProgressBar {
                color: #f0f0f0;
                font-size: 12px;
            }
        """)

    def activate_tab(self, index):
        # Функция активации вкладки меню
        self.stack_layout.setCurrentIndex(index)


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
