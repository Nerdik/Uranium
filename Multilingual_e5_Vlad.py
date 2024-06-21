from sentence_transformers import SentenceTransformer
import pandas as pd
import sqlite3
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
#Используем мультиангл из практического занятия

#класс для эмбеддинга
class TextDatabase:
    def __init__(self, db_path='RAG_seminar2.db', model_name='intfloat/multilingual-e5-base'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.model = SentenceTransformer(model_name)

    def find_nearest_text(self, text, k=5):
        task_vector = self.model.encode([text])[0]
        
        # Извлечение эмбеддингов из бд
        self.cursor.execute("SELECT Text, embeddings FROM texts")
        rows = self.cursor.fetchall()

        # Декодирование эмбеддингов и поиск косинусного расстояния
        embeddings = np.array([np.frombuffer(row[1], dtype=np.float32) for row in rows])
        similarities = cosine_similarity([task_vector], embeddings)[0]

        # найти индексы k ближайших
        nearest_indices = similarities.argsort()[-k:][::-1]

        # вернуть k ближайших
        nearest_text = [rows[i] for i in nearest_indices]
        return nearest_text

    def close(self):
        self.conn.close()
  

#получаем ближайшие слова для одного датафрейма, n ближайших значений, request- запрос
def get_words_from_multilingual_e5_base(test_texts, n, request,i):
    # Проверяем существование файла перед удалением (опционально)
    file_path = 'RAG_seminar'+str(i)+'.db'
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")
    else:
        print(f"Файл {file_path} не существует.")
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS texts
                (Text TEXT, embeddings BLOB)''')
    conn.commit()
    model = SentenceTransformer('intfloat/multilingual-e5-base')
    task_vectors = model.encode(
        test_texts.apply(
            lambda row: f"{row['text']}",
            axis=1
        ).tolist(),
        normalize_embeddings=True
    )

    task_vectors_bytes = [vector.tobytes() for vector in task_vectors]

    for i, row in test_texts.iterrows():
        cursor.execute(
            '''INSERT INTO texts (Text, embeddings)
            VALUES (?,  ?)''',
            (row['text'], task_vectors_bytes[i])
        )
    conn.commit()
    conn.close()
    
   
    td = TextDatabase(db_path=file_path)
    a = td.find_nearest_text(text=request,k=n)
    return a

