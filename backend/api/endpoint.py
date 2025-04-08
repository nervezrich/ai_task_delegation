# backend/main.py

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List
from ai.ai_task_delegator import assign_task_ai
from db.queries import fetch_users_tasks

router = APIRouter()

# Task request schema
class TaskRequest(BaseModel):
    task_id: str
    title: str
    description: str
    type_of_task: str
    priority_level: str
    due_date: str

@router.post("/task-delegate")
async def assign_tasks_ai_endpoint(tasks_to_delegate: List[TaskRequest]):
    # Convert Pydantic objects to list of dictionaries
    task_dicts = [task.dict() for task in tasks_to_delegate]

    existing_assignments = fetch_users_tasks()  # Function to get already assigned tasks
    assigned_task_ids = {task["task_id"] for task in existing_assignments} 

    duplicate_tasks = []

    # Filter out duplicates
    tasks_for_ai = []
    for task in tasks_to_delegate:
        task_id = task.task_id

        if task_id in assigned_task_ids:
            duplicate_tasks.append(task_id)
        else:
            tasks_for_ai.append(task.dict())

    # Only pass valid tasks to the AI
    assigned_tasks = assign_task_ai(tasks_for_ai)

    response = {"assigned_tasks": assigned_tasks}

    if duplicate_tasks:
        response["duplicate_tasks"] = duplicate_tasks
    
    return response

