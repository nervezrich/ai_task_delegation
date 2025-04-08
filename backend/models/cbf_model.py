import pandas as pd
from db.database import save_csv
from db.queries import fetch_users_tasks, fetch_unassigned_tasks
from .feature_processing import compute_similarity  # Importing the function

def assign_task(requested_tasks):
    """Assign only the tasks selected in the frontend to the best-matching users based on past successful tasks."""

    # Fetch past successful tasks (prioritize quality_score ≥ 8)
    past_tasks = fetch_users_tasks()
    if past_tasks.empty:  
        return {"message": "No past tasks available for comparison."}

    # Sort past tasks by quality score distance from 8 (higher scores are prioritized)
    past_tasks["score_distance"] = abs(past_tasks["quality_score"] - 0.8)
    past_tasks = past_tasks.sort_values(by=["score_distance"])
    past_tasks = past_tasks.to_dict(orient="records")

    # Fetch all unassigned tasks (to validate if the selected tasks exist)
    all_unassigned_tasks = fetch_unassigned_tasks()
    
    # Convert all unassigned tasks to a dictionary for fast lookup
    unassigned_tasks_dict = {task["task_id"]: task for task in all_unassigned_tasks}

    # Validate requested tasks (only allow tasks that exist in the unassigned list)
    valid_tasks = [task for task in requested_tasks if task["task_id"] in unassigned_tasks_dict]

    if not valid_tasks:
        return {"message": "No valid tasks found for assignment."}

    # Prepare past task data for similarity computation
    past_task_data = [{"type_of_task": task["type_of_task"], "priority_level": task["priority_level"]} for task in past_tasks]
    
    # Extract user IDs for tracking task ownership
    user_ids = [task["user_id"] for task in past_tasks]

    assigned_results = []
    for task in valid_tasks:
        # Compute similarity using the function from feature_processing
        similarities = compute_similarity(
            {"type_of_task": task["type_of_task"], "priority_level": task["priority_level"]},
            past_task_data
        )[0]
        
        # Ensure similarities is a 1D array
        similarities = similarities.flatten()  # Convert matrix to 1D array
        
        # Assign to the best match
        best_match_index = similarities.argmax()
        best_user = user_ids[best_match_index]

        # Log the assignment into task history
        task_record = {
            "user_id": best_user,
            "quality_score": 0,  # Will be updated later after completion
            "task_id": task["task_id"],
            "title": task["title"],
            "description": task["description"],
            "type_of_task": task["type_of_task"],
            "priority_level": task["priority_level"],
            "due_date": task["due_date"]
        }

        # Load existing task history, append new record, and save
        df = pd.read_csv("data/th.csv")
        df = df._append(task_record, ignore_index=True)
        save_csv(df, "data/th.csv")

        assigned_results.append({
            "task_id": task["task_id"],
            "assigned_user": best_user,
            "similarity_score": float(similarities[best_match_index])
        })

    return {"assignments": assigned_results}




