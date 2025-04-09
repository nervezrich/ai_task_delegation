# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from db.queries import save_csv, fetch_unassigned_tasks, fetch_users_tasks
# from models.cbf_model import assign_task
# from ai.train import retrain_model
# import pandas as pd

# router = APIRouter()

# @router.post("/assign_tasks")
# def assign_tasks_endpoint(requested_tasks: list[dict]):
#     """Assign tasks only if they exist, match the details in tasks.csv, and are not already assigned."""

#     all_unassigned_tasks = fetch_unassigned_tasks()
#     existing_assignments = fetch_users_tasks()  # Function to get already assigned tasks

#     # Convert task list from DataFrame to dictionaries for quick lookup
#     valid_tasks_dict = {task["task_id"]: task for task in all_unassigned_tasks}
#     assigned_task_ids = {task["task_id"] for task in existing_assignments}  # Set of assigned task IDs

#     valid_tasks = []
#     invalid_tasks = []
#     mismatched_tasks = []
#     duplicate_tasks = []

#     for task in requested_tasks:
#         task_id = task["task_id"]

#         # Check if the task has already been assigned
#         if task_id in assigned_task_ids:
#             duplicate_tasks.append(task_id)
#             continue  # Skip duplicate tasks

#         if task_id in valid_tasks_dict:
#             actual_task = valid_tasks_dict[task_id]  # Get actual task details
            
#             # Validate task details (compare each field)
#             mismatches = []
#             for key in ["title", "description", "type_of_task", "priority_level", "due_date"]:
#                 if task[key] != actual_task[key]:
#                     mismatches.append(key)

#             if mismatches:
#                 mismatched_tasks.append({"task_id": task_id, "mismatched_fields": mismatches})
#             else:
#                 valid_tasks.append(task)  # Add task if all details match and it's not a duplicate
#         else:
#             invalid_tasks.append(task_id)  # Task ID not found

#     # # If there are no valid tasks to assign, return an error
#     if not valid_tasks:
#         raise HTTPException(status_code=400, detail="No valid tasks found for assignment.")

#     # Assign only valid tasks
#     assigned_tasks = assign_task(valid_tasks)

#     response = {"assigned_tasks": assigned_tasks}

#     if invalid_tasks:
#         response["invalid_tasks"] = invalid_tasks  # Show task IDs that don't exist

#     if mismatched_tasks:
#         response["mismatched_tasks"] = mismatched_tasks  # Show fields that don't match

#     if duplicate_tasks:
#         response["duplicate_tasks"] = duplicate_tasks  # Show already assigned tasks

#     return response




# class UpdateScoreRequest(BaseModel):
#     user_id: str
#     task_id: str
#     new_score: float

# @router.post("/update_quality_score")
# def update_quality_score(request: UpdateScoreRequest):
#     """ Update the quality score of a user's past task """
#     file_path = "data/th.csv"
    
#     try:
#         df = pd.read_csv(file_path)

#          # Find the row that matches user_id and task_id
#         mask = (df["user_id"] == request.user_id) & (df["task_id"] == request.task_id)

#         if not mask.any():
#             return {"message": "Task not found for the user"}

#         # Update the quality score
#         df.loc[mask, "quality_score"] = request.new_score

#         # Save updated CSV
#         df.to_csv(file_path, index=False)

#         return {"message": "Task score updated successfully"}

#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Task history file not found")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/retrain_model")
# def retrain_model_endpoint():
#     result = retrain_model()
#     return result
