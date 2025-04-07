# import numpy as np
# import joblib
# from sklearn.metrics.pairwise import cosine_similarity
# from db.queries import fetch_successful_tasks  # Placeholder for fetching past successful tasks
# from .feature_processing import compute_similarity  # Importing the function

# # Load the encoder, scaler, Random Forest model, and user ID reverse map
# encoder = joblib.load("backend/models/encoder.joblib")
# scaler = joblib.load("backend/models/scaler.joblib")
# rf_model = joblib.load("backend/models/random_forest_task_assigner.joblib")
# user_id_reverse_map = joblib.load("backend/models/user_id_reverse_map.joblib")

# # def compute_similarity(task, past_task_data):
# #     """
# #     Computes similarity between the current task and past tasks.
# #     Uses the historical performance data (quality_score) for user matching.
# #     """
# #     # Task features: encode type_of_task and priority_level
# #     task_encoded = encoder.transform([[task["type_of_task"], task["priority_level"]]])

# #     # We don't need 'quality_score' for new tasks, so we only scale the other features
# #     task_features = task_encoded

# #     # Extract past task features: encode type_of_task and priority_level
# #     past_features = np.array([encoder.transform([[t["type_of_task"], t["priority_level"]]])[0] for t in past_task_data])
# #     # Extract corresponding quality scores for past tasks
# #     past_quality = np.array([t["quality_score"] for t in past_task_data])

# #     # Combine past task features and quality scores
# #     past_features_combined = np.hstack([past_features, past_quality.reshape(-1, 1)])

# #     # Compute cosine similarity between the new task and the past tasks
# #     similarities = cosine_similarity(task_features, past_features_combined)

# #     return similarities


# def assign_task(requested_tasks):
#     """
#     Assigns tasks to the most suitable users based on CBF algorithm.
#     Uses the past performance of users (quality_score).
#     """
#     past_tasks = fetch_successful_tasks()  # Fetch successful past tasks from the database
    
#     # Process requested tasks
#     assigned_tasks = []
#     for task in requested_tasks:
#         similarities = compute_similarity(task, past_tasks)

#         # Get the user with the highest similarity
#         best_match_index = similarities.argmax()
#         best_user = past_tasks[best_match_index]["user_id"]

#         # Assign the task to the best matching user
#         assigned_tasks.append({
#             "task_id": task["task_id"],
#             "assigned_user": best_user,
#             "similarity_score": float(similarities[0][best_match_index])
#         })

#     return assigned_tasks

