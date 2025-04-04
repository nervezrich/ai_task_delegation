from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_tasks(tasks):
    vectorizer = TfidfVectorizer()
    task_texts = [" ".join([task["type_of_task"], task["priority_level"]]) for task in tasks]
    return vectorizer.fit_transform(task_texts), vectorizer

def compute_similarity(new_task, past_tasks):
    """Compute cosine similarity between a new task and past successful tasks."""
    
    # Convert task dictionaries into text format
    past_task_matrix, vectorizer = preprocess_tasks(past_tasks)
    
    new_task_vector = vectorizer.transform([" ".join([new_task["type_of_task"], new_task["priority_level"]])])

    # Compute cosine similarity between the new task and past tasks
    similarities = cosine_similarity(new_task_vector, past_task_matrix)  # This ensures an array is returned
    
    return similarities  # Returns an array (not a scalar)
