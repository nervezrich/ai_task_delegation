import joblib
import numpy as np
import pandas as pd
import os
from sklearn.metrics.pairwise import cosine_similarity
from db.queries import (
    fetch_task_performance,
    get_users_in_project,
    fetch_pending_task_count_for_user,
    fetch_avg_quality_score_per_task_type
)

# Load trained model and preprocessing pipeline
model = joblib.load("ml/task_delegation_model.pkl")
preprocessing_pipeline = joblib.load("ml/preprocessing_pipeline.pkl")

def assign_task_ai(requested_tasks, project_id):
    try:
        past_tasks = fetch_task_performance(ProjectID=project_id)
        project_user_ids = get_users_in_project(project_id)

        if not project_user_ids:
            return {"message": "No users found in the project."}

        pending_tasks_map = fetch_pending_task_count_for_user(ProjectID=project_id, UserIDs=list(project_user_ids))

        if isinstance(past_tasks, list):
            if not past_tasks:
                return {"message": "No successful tasks found for comparison."}
            past_tasks = pd.DataFrame(past_tasks)
        elif past_tasks.empty:
            return {"message": "Past task data is empty."}

        task_assignments = []

        for task in requested_tasks:
            task_features = {
                "title": task.get("title", ""),
                "description": task.get("description", ""),
                "type_of_task": task["type_of_task"],
                "priority_level": task["priority_level"],
                "preferred_task": task.get("preferred_task", ""),
                "workload": 0,  # Dummy for new task
                "avg_quality_score": 0.0  # Dummy for new task
            }

            task_df = pd.DataFrame([task_features])
            task_vector = preprocessing_pipeline.transform(task_df)

            best_match = None
            best_similarity = float('-inf')

            for user_id in project_user_ids:
                user_past_tasks = past_tasks[past_tasks["UserID"] == user_id]

                if user_past_tasks.empty:
                    continue

                enriched_rows = []
                for _, user_task in user_past_tasks.iterrows():
                    try:
                        avg_quality_dict = fetch_avg_quality_score_per_task_type(ProjectID=project_id, UserID=user_id)
                        avg_quality_score = avg_quality_dict.get(user_task["typeOfTask"], 0.0)
                    except Exception:
                        avg_quality_score = 0.0

                    enriched_rows.append({
                        "title": user_task.get("title", ""),
                        "description": user_task.get("description", ""),
                        "type_of_task": user_task["typeOfTask"],
                        "priority_level": user_task["priorityLevel"],
                        "preferred_task": user_task.get("preferredTask", ""),
                        "workload": pending_tasks_map.get(user_id, 0),
                        "avg_quality_score": avg_quality_score
                    })

                user_past_df = pd.DataFrame(enriched_rows)
                user_vectors = preprocessing_pipeline.transform(user_past_df)

                similarities = cosine_similarity(task_vector, user_vectors)
                avg_similarity = np.mean(similarities)

                if avg_similarity > best_similarity:
                    best_similarity = avg_similarity
                    best_match = user_id

            task_assignments.append({
                "task_id": task["task_id"],
                "assigned_user": best_match
            })

        save_task_assignments_to_db(task_assignments)
        return {"assignments": task_assignments}

    except Exception as e:
        return {"message": f"Error processing tasks: {str(e)}"}

def save_task_assignments_to_db(assignments):
    assignments_df = pd.DataFrame(assignments)
    csv_file_path = 'data/task_assignments.csv'

    if not os.path.exists(csv_file_path):
        assignments_df.to_csv(csv_file_path, index=False, mode='w', header=True)
    else:
        assignments_df.to_csv(csv_file_path, index=False, mode='a', header=False)

    print(f"Task assignments saved to {csv_file_path}")
