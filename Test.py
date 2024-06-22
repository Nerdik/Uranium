from Get_dictionary_Michael import Get_DF_from_Dictionary, Get_Small_Dictionary_from_Excel, select_excel_files, Get_ALL_Dictionary_from_Excel
from Multilingual_e5_Vlad import get_words_from_multilingual_e5_base
#from Multilingual_Alex import get_words_from_multilingual_bert
import pandas as pd
import copy
import os
from Ask_Gigachat import Get_Answer_LLM

#получение словаря следующего формата: key:запросный столбец пользователя, value: словарь малый и большой неочищенные.
def Get_global_dict(request, quantity, path):
    #получаем словарь с заголовками
    s_small=Get_Small_Dictionary_from_Excel(path)
    print('Малый словарь нефильтрованный',s_small)
    #получаем весь словарь
    s_big=Get_ALL_Dictionary_from_Excel(path)
    print('Большой словарь нефильтрованный: ',s_big)
    # Создание нового словаря, в котором ключи это запросы пользователя, глобальный словарь, в него входят девственные большой и малый словари
    global_dict = {key: [copy.deepcopy(s_big),copy.deepcopy(s_small)] for key in request}
    print('Глобальный словарь нефильтрованный: ',global_dict)
    i=0
    # Проход по всем ключам словаря и передача значения s в функцию
    for key in global_dict:
        i=i+1
        s_value = global_dict[key][1]  # Получение значения s из списка
        s_value_big=global_dict[key][0]
        print('Малый словарь для передачи в multi для значения пользователя '+str(key)+': ',s_value)
        # #получаем датафрейм из малого словаря для передачи в multi
        test_texts=Get_DF_from_Dictionary(s_value)
        print('Dataframe для передачи в multi для значения пользователя '+str(key)+': ',test_texts)
        #получаем ответ в виле списка заголовков [list]
        answer= get_words_from_multilingual_e5_base(test_texts,quantity,key,i)
        #Формируем лист из ответа:    
        new_list = [item[0] for item in answer]
        answer=new_list
        print('Multilingul вернул для значения пользователя '+str(key)+': ',answer)
        # Удаление значений из малого словаря
        for key1 in s_value:
            s_value[key1] = [value for value in s_value[key1] if value in answer]
        print('Отформотированный малый словарь для значения пользователя '+str(key)+': ',s_value) 
        # Удаление значений из большого словаря
        for outer_key in s_value_big:
            s_value_big[outer_key] = {k: v for k, v in s_value_big[outer_key].items() if k in answer}
        print('Отформатированный большой словарь для значения пользователя'+str(key)+': ',s_value_big)
        global_dict[key]=[copy.deepcopy(s_value_big),copy.deepcopy(s_value)]
    return global_dict

# #In[0]
# #выбираем файлы-> можно получить из интерфейса, учесть r перед путем
# path=select_excel_files()
# #In[1]
# #Запрос пользователя текстом
# request_text=input("Введите запрос: ")
# print(request_text)
# #промт в гигачат
# request_promt=f'Из следующего предложения вычлени заголовки для таблицы в виде списка: {request_text}'
# print(request_promt)
# #получаем ответ от гигачата
# request= Get_Answer_LLM(request_text,request_promt)
# print (request)
# #Постобработка ответа гигачата
# request = request.splitlines()
# # Удаление номеров элементов
# request = [элемент.split('.', 1)[-1].strip() for элемент in request if элемент.strip()]
# request = [item for item in request if "Заголовки" not in item]
# print(request)
# #In[1]
# #задаем количество возвращаемых заголовков-> из интерфейса
# quantity =3
# #получение глобального словаря
# global_dict=Get_global_dict(request,quantity, path)
# print('Отформатированный глобальный словарь',global_dict)

# #In[0]
# # Создание DataFrame для экспорта в Excel
# df = pd.DataFrame(columns=global_dict.keys())
# # Добавление данных в DataFrame
# i=-1
# for key in global_dict:
#     i=i+1
#     values=[]
#     #Извлекаем большие словари для каждого ключа
#     s_big=global_dict[key][0]
#     #Заходим внутрь, тут еще один словарь, где ключи это заголовки
#     for excel_key in s_big:
#         s_excel_big= s_big[excel_key]
#         #Заходим в последнюю матрешку,в словарь, где ключи заголовки
#         for zagolovok_excel_key in s_excel_big:
#             values.extend(s_excel_big[zagolovok_excel_key].values)
#     # Проверяем, нужно ли изменить размер DataFrame
#     num_rows = len(df)
#     num_values = len(values)
#     if num_values > num_rows:
#         # Увеличиваем DataFrame до нужного размера
#         df = df.reindex(range(num_values))
#     elif num_values < num_rows:
#         # Обрезаем DataFrame до нужного размера
#         df = df.iloc[:num_values]        
#     df.iloc[:, i] = values            
# # Сохранение DataFrame в Excel
# if os.path.exists('output.xlsx'):
#     os.remove('output.xlsx')
#     print(f"Файл {'output.xlsx'} успешно удален.")
# else:
#     print(f"Файл {'output.xlsx'} не существует.")
# df.to_excel('output.xlsx', index=False)
# #In[1]

# # #Вычитание из большого словаря маленького
# #         s_big=Get_ALL_Dictionary_from_Excel(path)
# #         # Получаем путь к файлу и лист
# #         file_path = list(s.keys())[0]

# #         # Получаем список допустимых столбцов из первого словаря
# #         valid_columns = s[file_path]

# #         # Отфильтровываем столбцы второго словаря
# #         filtered_data = {key: value for key, value in s_big[file_path].items() if key in valid_columns}

# #         # Обновляем второй словарь
# #         filtered_dict2 = {file_path: filtered_data}

# #         # Печатаем результат
# #         print('Отформатированный список:',filtered_dict2)
