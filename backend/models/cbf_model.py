import pandas as pd
from db.database import load_csv, save_csv
from db.queries import fetch_successful_tasks, fetch_unassigned_tasks
from sklearn.metrics.pairwise import cosine_similarity

def assign_task(new_tasks):
    """Assign one or multiple tasks to the best-matching users based on past successful tasks."""
    
    # Fetch past successful tasks (only with quality_score ≥ 8)
    past_tasks = fetch_successful_tasks()
    if past_tasks.empty:  
        return {"message": "No past tasks available for comparison."}
    
    past_tasks = past_tasks.to_dict(orient="records")

    # Fetch all unassigned tasks from tasks.csv
    all_unassigned_tasks = fetch_unassigned_tasks()  # Returns list of dicts

    # Validate requested task IDs
    valid_task_ids = {task["task_id"] for task in all_unassigned_tasks}

    # If only one task is given, wrap it in a list
    if isinstance(new_tasks, dict):  
        new_tasks = [new_tasks]

    # Filter out invalid task IDs
    valid_tasks = [task for task in new_tasks if task["task_id"] in valid_task_ids]
    if not valid_tasks:
        return {"message": "No valid tasks found for assignment."}

    # Convert task attributes into numerical format
    type_task_mapping = {task: i for i, task in enumerate(set(task["type_of_task"] for task in past_tasks))}
    priority_mapping = {"low": 0, "neutral": 1, "high": 2}

    past_task_vectors = [
        [type_task_mapping[task["type_of_task"]], priority_mapping[task["priority_level"].lower()]]
        for task in past_tasks
        if task["type_of_task"] in type_task_mapping and task["priority_level"].lower() in priority_mapping
    ]

    user_ids = [task["user_id"] for task in past_tasks]

    if not past_task_vectors:
        return {"message": "No valid past tasks found for similarity comparison."}

    assigned_results = []
    for task in valid_tasks:
        # Convert the new task into a vector
        new_task_vector = [
            type_task_mapping.get(task["type_of_task"], -1),
            priority_mapping.get(task["priority_level"].lower(), -1)
        ]

        if -1 in new_task_vector:
            assigned_results.append({
                "task_id": task["task_id"],
                "message": "Invalid task attributes, cannot match."
            })
            continue

        # Compute cosine similarity
        similarities = cosine_similarity([new_task_vector], past_task_vectors)[0]

        # Assign to the best match or closest match if no perfect similarity
        if max(similarities) > 0:
            best_match_index = similarities.argmax()
            best_user = user_ids[best_match_index] 
        else:
            best_user = user_ids[similarities.argmax()]  # Closest match (fallback)

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

        df = pd.read_csv("data/task_history.csv")
        df = df._append(task_record, ignore_index=True)
        save_csv(df, "data/task_history.csv")

        assigned_results.append({
            "task_id": task["task_id"],
            "assigned_user": best_user,
            "similarity_score": float(similarities[similarities.argmax()])
        })

    return {"assignments": assigned_results}
