# from .database import get_db_connection

# def fetch_successful_tasks():
#     conn = get_db_connection()
#     if conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT user_id, quality_score, type_of_task, priority_level FROM task_history WHERE quality_score >= 8")
#         result = cursor.fetchall()
#         conn.close()
#         return result
#     return []

# def fetch_users():
#     conn = get_db_connection()
#     if conn:
#         cursor = conn.cursor()
#         cursor.execute("SELECT user_id, name, skills FROM users")
#         result = cursor.fetchall()
#         conn.close()
#         return result
#     return []

import pandas as pd
from .database import load_csv, save_csv

def fetch_successful_tasks():
    """ Fetch past successful tasks (quality_score ≥ 8) from CSV """
    df = load_csv("data/task_history.csv")
    if df is not None:
        return df[df["quality_score"] >= 8.00][["user_id", "quality_score", "type_of_task", "priority_level"]]
    return pd.DataFrame(columns=["user_id", "quality_score", "type_of_task", "priority_level"])

def fetch_unassigned_tasks():
    """Fetch all tasks from ta sks.csv (since all are unassigned initially)."""
    df = load_csv("data/tasks.csv")
    return df.to_dict(orient="records") if df is not None else []

def fetch_users_tasks():
    """ Fetch all users from CSV """
    df = load_csv("data/task_history.csv")
    return df.to_dict(orient="records") if df is not None else []

def update_task_score(user_id, task_id, score):
    """ Update task quality score after task completion """
    df = pd.read_csv("data/task_history.csv")
    df.loc[(df["user_id"] == user_id) & (df["task_id"] == task_id), "quality_score"] = score
    save_csv(df, "data/task_history.csv")
    return {"message": "Task quality score updated."}

