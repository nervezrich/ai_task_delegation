# backend/main.py

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import List
from ai.ai_task_delegator import assign_task_ai

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
async def assign_tasks_ai_endpoint(tasks: List[TaskRequest]):
    # Convert Pydantic objects to list of dictionaries
    task_dicts = [task.dict() for task in tasks]
    
    # Call the AI delegation function
    result = assign_task_ai(task_dicts)
    
    return result
