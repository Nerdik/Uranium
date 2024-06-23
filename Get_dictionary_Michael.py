import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

'''
Класс-обработчик таблиц excel, возвращает словарь , где ключи это названия файла+листа, а значения это словари, в котором ключи это заголовки, а значения это данные
'''
class Xls2Col():

    '''
    Инициализация через список имен
    
    '''
    def __init__(self, filePathList):

            self.ddmain = {}
            self.ddsmall = {}
            self.ddkey = []
            cc = 0
            
            ii = 0
            while ii < len(filePathList):
                xlsf = pd.ExcelFile(filePathList[ii])
                filename = filePathList[ii].split('\\')[-1]
                
                jj = 0
                while jj < len(xlsf.sheet_names):                
                    df = xlsf.parse(xlsf.sheet_names[jj])
                    dkey = '' + filename + ' ; ' + xlsf.sheet_names[jj]
                    # print(jj)
                    print('№  'f"{cc}  " + dkey + '    size of sheet ' + f"{df.size}")
                    if df.size > 0:
                        headLine,dd = Xls2Col.CreateCollection(df)
                        if headLine != False:
                            # dkey = '' + filename + ' ; ' + xlsf.sheet_names[jj]
                            # print(dkey + '______' + df.size)
                            self.ddkey.append(dkey)
                            self.ddmain[dkey] = dd
                            self.ddsmall[dkey] = headLine
                        else:
                            print('!!! ' + dkey + ' headline wasnt found')
                    else:
                        self.ddmain[dkey] = 'sheet is empty'
                        self.ddsmall[dkey] = 'sheet is empty'
                        print('!!! ' + dkey + ' sheet is empty')
                    cc += 1
                    jj += 1

                ii += 1
    '''
    Проверка строки на принадлежность к числам
    '''
    def IsNumber(str):
        if pd.isnull(str):
            return False
        else:
            try:
                float(str)
                return True
            except ValueError:
                return False

    '''
    '''
    def WhatInCell(xx):
        marker = -1
        try:
            # case cell = number
            float(xx)
            if (float(xx) == 0):
                #case cell = zero
                marker = 0
            else:
                #case cell = non-zero
                marker = 1
        except ValueError:
            # case cell = string
            marker = 2
        
        return marker
 
    '''
    Отметки таблицы
    '''
    def MarkDataFrame(df):
       
        ii = 0 #left-right
        jj = 0 #up-down
        countInColumns = np.zeros(df.columns.size)                            #elements in col
        countInRows = np.zeros(df[df.columns[ii]].size)                       #elements in row
        counter = [0,0,0]                                                     #blind counter
        counterLine = np.zeros([df[df.columns[ii]].size,3])                   #cell type database
        markerDF = np.zeros([df[df.columns[ii]].size,df.columns.size]) - 5    #code table
        
        #up->down
        while jj < df[df.columns[ii]].size:
            #left->right
            while ii < df.columns.size:
                # case cell is not empty
                if not pd.isnull(df[df.columns[ii]][jj]):
                    countInColumns[ii] +=1
                    countInRows[jj] += 1
                    
                    try:
                        # case cell = number
                        float(f'{df[df.columns[ii]][jj]}')
                        if (float(df[df.columns[ii]][jj]) == 0):
                            #case cell = zero
                            markerDF[jj,ii] = 0
                            counter[0] += 1
                        else:
                            #case cell = non-zero
                            markerDF[jj,ii] = 1
                            counter[1] += 1
                    except ValueError:
                        # case cell = string
                        markerDF[jj,ii] = 2
                        counter[2] += 1
                # case cell is empty
                else:
                    markerDF[jj,ii] = -1
                ii += 1

            counterLine[jj,0] = int(counter[0])
            counterLine[jj,1] = int(counter[1])
            counterLine[jj,2] = int(counter[2])
            jj += 1
            ii = 0
            counter = [0,0,0]
            
        return counterLine, [countInColumns,countInRows], markerDF


    '''
    Содержание первой строки DataFrame
    DataFrame (pandas.core.frame.DataFrame) - это набор столбцов (pandas.core.series.Series)
    функция pandas.ExcelFile.parse(...) создает DataFrame, названием столбцов которого является первая строка
    Чтобы восстановить таблицу необходимо извлечь первую строку из названий столбцов
    Вход - DataFrame
    Выход - список [позиция (номер столбца) , содержание]
    '''
    def FirstRowDataFrame(df):
        ii = 0
        firstRow = []
        while ii < df.columns.size:
            if df.columns[ii] != ('Unnamed: ' + str(ii)):
                firstRow.append([ii, df.columns[ii]])
            ii += 1
        return firstRow

    '''
    Функция для анализа содержания таблицы
    '''
    def EmptyDataFrame(df):
        cline, clims, mdf = Xls2Col.MarkDataFrame(df)
        trsh = []
        trsh.append(0.10) #columns are not empty if _ count > median(countOfElementsInAllColumns) * trashold 
        trsh.append(0.85) #row is zeros if _ zeros count > countOfElementsInRow * trashold
        trsh.append(0.25) #row is header if _ str count > median(countOfElementsInAllRows) * trashold
        trsh.append(0.10) #row is data if _ numbers count > median(countOfElementsInAllRows) * trashold

        ii = 0
        notEmptyColumns = []
        while ii < clims[0].size:
            if clims[0][ii] > np.max(clims[0])*trsh[0]:
                notEmptyColumns.append(ii)
            ii += 1

        jj = 0
        rowsStr = []
        rowsZero = []
        rowsQuestion = []
        rowsWithData = []
        rowHeaderStart = -1
        while jj < cline.shape[0]:
            csum = cline[jj][0] + cline[jj][1] + cline[jj][2]
            if (csum != clims[1][jj]):
                rowsQuestion.append(jj)
                print(f'Row {jj} with unmarked instance')
            if cline[jj][2] > 0:
                rowsStr.append(jj)

            if csum > 0:
                if cline[jj][0] > csum*trsh[1]:
                    rowsZero.append(jj)
                
                if (cline[jj][2] > csum*trsh[1] 
                    and cline[jj][2] > np.max(clims[1])*trsh[2]
                    and rowHeaderStart < 0):
                    # print(np.median(clims[1])*trsh[2])
                    rowHeaderStart = jj
                
                if cline[jj][1] > csum*trsh[3]:
                    rowsWithData.append(jj)
            jj += 1
        
        return notEmptyColumns,rowHeaderStart,rowsWithData,[rowsStr,rowsZero,rowsQuestion]
    

    '''
    
    '''
    def CreateNewDataFrame(df):
        notEmpCol, rhstart, rdata,qq = Xls2Col.EmptyDataFrame(df)

        dfnew = pd.DataFrame()
        ii = 0
        while ii < len(notEmpCol):
            dfnew = pd.concat([dfnew, df[df.columns[notEmpCol[ii]]]], ignore_index=True,axis = 1)
            ii += 1

        return dfnew, rhstart, rdata

    '''
    
    '''
    def CreateCollection(dfraw):
        df, rhstart, rdata = Xls2Col.CreateNewDataFrame(dfraw)
        headList = Xls2Col.GetHead(df,rhstart)
        
        ii = 0
        jj = 0
        iStr = ''
        headLine = []
        
        if headList == -1:
            return False, False
        else:
            while ii < len(headList):
                while jj < len(headList[ii]):
                    if jj == 0:
                        iStr = iStr + headList[ii][jj] + ' ;'
                    else:
                        iStr = iStr + ' ' + headList[ii][jj]
                    jj += 1
                headLine.append(iStr)
                iStr = ''
                ii += 1
                jj = 0
    
            dd = {}
            ii = 0
            while ii < len(headLine):
                # dd.update(headline[ii] , df[df.columns[ii]][rdata])
                dd[headLine[ii]] = df[df.columns[ii]][rdata]
                ii += 1
                 
            return headLine, dd
            
    
    '''
    Формирование списка из шапки таблицы
    Функция проходит по шапке, пропуская пустые ячейки и останавливаясь при встрече чисел

    Ограничения
    Предполагается, что объединены (в экселе) могут быть только верхние ячейки
    Предполагается, что шапка не содержит числовые ячейки
    
    Входные аргументы
    df - обрабатываемый DataFrame
    headLineFieldsTrshld - достаточное количество ячеек в строке, чтобы считать её началом шапки таблицы (для поиска первой строки)
    headLineMaxRows - максимальное количество строк в шапке

    Выходные данные
    Список того, что содержится в шапке
    Длина списка равна количеству столбцов таблицы, т.к. пустое значение в первой ячейке воспринимается как объединение экселя
    Элементы списка - то, что содержится в столбце сверху-вниз, по порядку (можно сделать и прост через пробел)
    '''
    def GetHead(df, headLineStart, headLineMaxRows = 5):

            if (headLineStart >= df.shape[0]):
                print('headLineStart is out of range')
                return (-1)

            ii = 0                 # горизонтальный
            jj = 0                 # вертикальный
            iiref = 0              # ссылочный, если было объединение и ячейка пуста
            fullFieldName = []     # список для полного столбца
            headLine = []          # полный список

            # Цикл от столбца к столбцу по строкам
            while ii < df.columns.size:
                while (jj < headLineMaxRows):

                    # Проверка верхнего элемента шапки
                    # Допущение: только верхний элемент имеет горизонтальное объединение ячеек => ячейки правее - пусты
                    if (jj == 0):
                        # Если первая ячейка шапки пуста (на всякий случай)
                        if (pd.isnull(df[df.columns[ii]][jj + headLineStart])) and (iiref == 0):
                            # ii += 1
                            break
                        # Если первая ячейка шапки не пуста
                        elif (not pd.isnull(df[df.columns[ii]][jj + headLineStart])):
                            iiref = ii
                            fullFieldName.append(df[df.columns[ii]][jj + headLineStart])
                            jj += 1
                        # Случай объединения ячеек: верхняя пуста, но в предыдущем столбце уже было значение
                        # Отсюда баг слишком длинного списка, если в файле есть рандомная непустая ячейка далеко справа (чуть позже пофиксится)
                        elif (pd.isnull(df[df.columns[ii]][0 + headLineStart])) and (iiref > 0):
                            fullFieldName.append(df[df.columns[iiref]][0 + headLineStart])
                            jj += 1

                    else:
                        # на всякий случай
                        if (jj + headLineStart >= df[df.columns[ii]].size):
                            print('headline start is out of range')
                            return (-1)
                        else:
                            # Если встречается число, то считаем, что дошли до значений и шапка закончена - переход на новый столбец
                            if (Xls2Col.IsNumber(df[df.columns[ii]][jj + headLineStart])):
                                # print ("NUMBER",ii,"    ",jj)
                                # ii += 1
                                # jj = 0
                                break
                            else:
                                # Если ячейка пуста, то переход на новую строку
                                if (pd.isnull(df[df.columns[ii]][jj + headLineStart])):
                                    jj += 1
                                else:
                                    # Если ячейка не пуста и не число - добавь значение в список "столбца" и перейди на новую строку
                                    fullFieldName.append(df[df.columns[ii]][jj + headLineStart])
                                    jj += 1

                # Запиши список столбца в главный список, перейди на новый столбец и очисти счетчик строк и список столбца
                headLine.append(fullFieldName)
                fullFieldName = []
                ii += 1
                jj = 0

            return headLine
        
    '''
    Функция поиска шапки таблицы на странице экселя
    В разных файлах таблица начинается с разных строк
    Метод очень топорный, но на имеющихся примерах - рабочий

    Входные аргументы 
    df - pd.DataFrame для поиска
    headLineFieldsTrshld - достаточное количество ячеек в строке, чтобы считать её началом шапки таблицы 
    (очень мешаются всякие вводные слова в первых ячейках, это некий порог)

    Выходные данные
    headLineStart - номер строки, на которой начинается шапка таблицы
    lineFieldsCount - количество непустых ячеек в каждой строке таблицы
    '''
    
    def Find_headline(df, headLineFieldsTrshld = 5):
    
        ii = 0
        jj = 0
        counter = 0
        lineFieldsCount = np.zeros(df[df.columns[ii]].size)

        # пробежка по таблице
        # если найдено ненулевое значение, плюсани счетчик
        while ii < df.columns.size:
            while jj < df[df.columns[ii]].size:
                if not pd.isnull(df[df.columns[ii]][jj]):
                    lineFieldsCount[jj] += 1
                jj += 1
            ii += 1
            jj = 0

        # Если найдется строка с числом элементов больше порогового значения - она будет считаться первой строкой шапки
        nn = 0
        while nn < lineFieldsCount.size:
            if (lineFieldsCount[nn] >= headLineFieldsTrshld):
                headLineStart = nn
                break
            else:
                nn += 1
                    
        return headLineStart, lineFieldsCount
    
    # DEBUG PRINTS
    # print(self.features_table.at[nn,kk])   
    # print('Done')

# Извлечение значений из словаря и преобразование в DataFrame с одним столбцом 'text'
def Get_DF_from_Dictionary(dict,key_sheet):
    values = (dict[key_sheet])
    df = pd.DataFrame(values, columns=['text'])
    return df

#получаем весь словарь
def Get_Small_Dictionary_from_Excel(filePathList):
    
    #все выполнение в инициализации
    sssolve = Xls2Col(filePathList)

    #вернет словарь только с заголовками
    return sssolve.ddsmall   
  
#получаем меньший словарь, в котором есть только названия заголовков
def Get_ALL_Dictionary_from_Excel(filePathList):
    #все выполнение в инициализации
    sssolve = Xls2Col(filePathList)

    #вернет весь словарь
    return sssolve.ddmain   

#функция загрузки файлов 
def select_excel_files():
    # Создаем корневое окно и скрываем его
    root = tk.Tk()
    root.withdraw()

    # Разрешаем пользователю выбрать несколько файлов
    file_paths = filedialog.askopenfilenames(
        title="Выберите файлы Excel",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    # Преобразуем выбранные пути в список строк с префиксом r
    filePathList = [rf'{Path(path)}' for path in file_paths]
        
    # Преобразуем пути в формат списка
    file_path_list = list(file_paths)

    return file_path_list

def CreateDF_FromGlobalDict(data,quantity):

    # Инициализируем пустой список для строк
    rows = []
    # Получаем первый ключ словаря
    first_key = next(iter(data))

    print(data[first_key][1].keys()) 

    # Получаем заголовки из ключей первого элемента
    columns = list(data[first_key][1].keys())
    # Добавляем пустой заголовок в начало списка заголовков
    columns.insert(0, '')
    # Создаем пустой DataFrame с заданными заголовками
    df = pd.DataFrame(columns=columns)
    # Проходим по ключам словаря и заполняем строки
    for key_req in data.keys():
        for i in range(quantity):
            print('Шаг ',i)
            row = []
            if i==0:
                row.append(key_req)
            else:
                row.append('')
            print('Добавили запрос пользователя',key_req)
            print('Пока строка выглядит так: ',row)
            for key_sheets in data[key_req][1].keys():
                small_dick=data[key_req][1]
                print('ЩИИИИИИТ',key_sheets)
                print('Малый словарь',small_dick)
                print('Значения по листу экселя: ',small_dick[key_sheets])
                row.append(small_dick[key_sheets][i])
                print('Промежуточная строка выглядит так: ',row)
            print('Ккакой раув',row)         
            # Добавление новой строки
            if len(df)==0:
                df.loc[0] = row
            else:
                df.loc[len(df)] = row
    
    return df

def CreateDF_FromGlobalDict2(gd,NN):

    df_dict = {}
    Col2Req = []
    for req in gd.keys():
        for ii in range(NN):
            Col2Req.append(req)
        df_dict.update({"User request" : Col2Req})
        Col2Req = []
        for sheets in gd[req][0].keys():
            df_dict.update({sheets : gd[req][0][sheets]})
    print(df_dict)    
    df = pd.DataFrame(df_dict)
    return df