# import pandas as pd
# import numpy as np
# from transformers import BertModel, BertTokenizer
# import torch
# import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from sklearn.metrics.pairwise import cosine_similarity

# #получаем ближайшие слова для одного датафрейма, n ближайших значений, request- запрос
# def get_words_from_multilingual_bert(data, n, request):
#     # Загрузка модели и токенизатора
#     model = BertModel.from_pretrained('bert-base-multilingual-cased')
#     tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
#     # Предобработка текста
#     stop_words = set(stopwords.words('russian'))
#     lemmatizer = WordNetLemmatizer()
#     processed_text = []
#     for phrase in data['text']:
#         tokens = [lemmatizer.lemmatize(word) for word in phrase.lower().split() if word not in stop_words]
#         processed_text.append(' '.join(tokens))
#     # Функция для получения векторного представления фразы
#     def model_encode(phrase):
#         input_ids = torch.tensor([tokenizer.encode(phrase, add_special_tokens=True)])
#         with torch.no_grad():
#             last_hidden_states = model(input_ids)[0]
#         phrase_embedding = torch.mean(last_hidden_states, dim=1).squeeze().numpy()
#         return phrase_embedding
#     # Функция для поиска наиболее похожих фраз
#     def find_most_similar_phrases(query_phrase, top_n=n):
#         # Получаем векторное представление заданной фразы
#         query_embedding = model_encode(query_phrase)
#         # Вычисляем косинусное сходство между векторами
#         similarities = cosine_similarity([query_embedding], phrase_embeddings)[0]
#         # Находим наиболее похожие фразы
#         sorted_indices = np.argsort(similarities)[::-1][:top_n]
#         most_similar_phrases = [processed_text[i] for i in sorted_indices]
#         similarity_scores = [similarities[i] for i in sorted_indices]
#         return most_similar_phrases, similarity_scores
#     # Получение векторных представлений фраз
#     phrase_embeddings = []
#     for phrase in processed_text:
#         input_ids = torch.tensor([tokenizer.encode(phrase, add_special_tokens=True)])
#         with torch.no_grad():
#             last_hidden_states = model(input_ids)[0]
#         phrase_embedding = torch.mean(last_hidden_states, dim=1).squeeze().numpy()
#         phrase_embeddings.append(phrase_embedding)
#     # Пример использования
#     print(data)
#     query_phrase = request
#     most_similar_phrases, similarity_scores = find_most_similar_phrases(query_phrase)
#     phrase_list = []
#     print("Наиболее похожие фразы:")
#     for i, (phrase, score) in enumerate(zip(most_similar_phrases, similarity_scores), start=1):
#         print(f"{i}. '{phrase}' (similarity: {score:.4f})")
#         phrase_list.append(phrase)
#     return phrase_list

