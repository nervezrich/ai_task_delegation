from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_tasks(tasks):
    vectorizer = TfidfVectorizer()
    task_texts = [" ".join([task[2], task[3]]) for task in tasks]  # type_of_task + priority_level
    return vectorizer.fit_transform(task_texts), vectorizer

def compute_similarity(new_task, past_tasks):
    task_matrix, vectorizer = preprocess_tasks(past_tasks)
    new_task_vector = vectorizer.transform([" ".join([new_task['type_of_task'], new_task['priority_level']])])
    return cosine_similarity(new_task_vector, task_matrix)
  