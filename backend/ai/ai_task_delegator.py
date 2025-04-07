# ai_task_delegator.py

import joblib
import numpy as np
import pandas as pd
from db.queries import fetch_unassigned_tasks, fetch_successful_tasks
from db.database import save_csv

# Load model and tools
model = joblib.load("backend/models/random_forest_task_assigner.joblib")
encoder = joblib.load("backend/models/encoder.joblib")
scaler = joblib.load("backend/models/scaler.joblib")
reverse_map = joblib.load("backend/models/user_id_reverse_map.joblib")

def assign_task_ai(requested_tasks):
    successful_tasks = fetch_successful_tasks()

    # Convert to DataFrame if it's a list
    if isinstance(successful_tasks, list):
        if not successful_tasks:
            return {"message": "No successful tasks found for comparison."}
        successful_tasks = pd.DataFrame(successful_tasks)
    elif successful_tasks.empty:
        return {"message": "No successful tasks found for comparison."}


    # Compute avg_quality_score & task_count
    summary = successful_tasks.groupby(["user_id", "type_of_task", "priority_level"]).agg(
        avg_quality_score=("quality_score", "mean"),
        task_count=("quality_score", "count")
    ).reset_index()

    # Validate and assign
    assigned = []
    for task in requested_tasks:
        matched = summary[
            (summary["type_of_task"] == task["type_of_task"]) &
            (summary["priority_level"] == task["priority_level"])
        ]

        if matched.empty:
            continue  # No history

        # Select the user with best avg score
        best = matched.sort_values(by=["avg_quality_score", "task_count"], ascending=False).iloc[0]

        # Encode new task
        task_encoded = encoder.transform([[task["type_of_task"], task["priority_level"]]])
        task_scaled = scaler.transform([[best["avg_quality_score"], best["task_count"]]])
        features = np.hstack([task_encoded, task_scaled])

        pred_label = model.predict(features)[0]
        user_id = reverse_map[pred_label]

        # Save to CSV
        history = pd.read_csv("data/th.csv")
        record = {
            "user_id": user_id,
            "quality_score": 0,
            "task_id": task["task_id"],
            "title": task["title"],
            "description": task["description"],
            "type_of_task": task["type_of_task"],
            "priority_level": task["priority_level"],
            "due_date": task["due_date"]
        }
        history = history._append(record, ignore_index=True)
        save_csv(history, "data/th.csv")

        assigned.append({
            "task_id": task["task_id"],
            "assigned_user": user_id
        })

    return {"assignments": assigned}
