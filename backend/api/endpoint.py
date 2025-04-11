from fastapi import APIRouter, Path
from pydantic import BaseModel
from uuid import UUID  # Import UUID
from typing import List
from ai.assign_task_ai import assign_task_ai
from db.queries import fetch_task_performance

router = APIRouter()

# Task request schema
class TaskRequest(BaseModel):
    task_id: UUID  # Use UUID for task_id if it's a UUID
    title: str
    description: str
    type_of_task: str
    priority_level: str
    due_date: str

@router.post("/task-delegate/{project_id}")
async def assign_tasks_ai_endpoint(
    tasks_to_delegate: List[TaskRequest],
    project_id: UUID = Path(..., description="The ID of the project")  # Use UUID here for project_id
):
    # Fetch existing assignments to check for duplicates
    existing_assignments = fetch_task_performance(ProjectID=project_id)  # Ensure the function supports project_id
    assigned_task_ids = {task["TaskID"] for task in existing_assignments}

    duplicate_tasks = []
    tasks_for_ai = []

    # Filter out duplicate tasks
    for task in tasks_to_delegate:
        task_id = task.task_id

        if task_id in assigned_task_ids:
            duplicate_tasks.append(task_id)
        else:
            tasks_for_ai.append(task.dict())  # Convert Pydantic object to dictionary

    # Only pass valid tasks to the AI system for assignment
    assigned_tasks = assign_task_ai(tasks_for_ai, project_id=project_id)  # Pass dynamic project_id

    # Prepare the response
    response = {"assigned_tasks": assigned_tasks}

    if duplicate_tasks:
        response["duplicate_tasks"] = duplicate_tasks

    return response
