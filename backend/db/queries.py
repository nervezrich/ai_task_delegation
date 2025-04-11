from .database import get_db_connection
import pandas as pd
from uuid import UUID

def fetch_task_performance(ProjectID: UUID):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    p."UserID",
                    u."first_name",
                    u."last_name",
                    p."TaskID",
                    t."title",
                    t."description",
                    t."typeOfTask",
                    t."priorityLevel",
                    t."dueDate",
                    p."QualityScore"
                FROM 
                    "Performance" p
                JOIN "Tasks" t ON p."TaskID" = t."taskId"
                JOIN "User" u ON p."UserID" = u."UserID"
                WHERE 
                    p."ProjectID" = %s
            """
            cursor.execute(query, (str(ProjectID),))  # convert UUID to string
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            conn.close()

            result = [dict(zip(columns, row)) for row in rows]
            return result
        except Exception as e:
            print("Error fetching past tasks:", e)
            conn.close()
            return []
    return []


def fetch_pending_task_count_for_user(ProjectID: UUID, UserIDs: list):
    conn = get_db_connection()
    if conn:
        try:
            # Ensure UserIDs is a list or tuple (avoid set type)
            if isinstance(UserIDs, set):
                UserIDs = list(UserIDs)  # Convert set to list

            cursor = conn.cursor()
            query = """
                SELECT 
                    COUNT(*) AS pending_task_count
                FROM 
                    "Tasks" t
                WHERE 
                    t."ProjectID" = %s
                    AND t."AssignedTo" = ANY(%s::uuid[])  -- Use UUID array for comparison
                    AND t."completedAt" IS NULL  -- Filter for tasks that are not completed
            """
            cursor.execute(query, (str(ProjectID), UserIDs))  # Pass UserIDs as list
            rows = cursor.fetchall()
            conn.close()

            # Extract the count from the result
            pending_task_count = rows[0][0] if rows else 0
            return {"pending_task_count": pending_task_count}

        except Exception as e:
            print("Error counting pending tasks:", e)
            conn.close()
            return {"message": f"Error: {str(e)}"}
    return {"message": "Database connection failed."}


def fetch_avg_quality_score_per_task_type(ProjectID: UUID, UserID: UUID):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT 
                    t."typeOfTask",
                    AVG(p."QualityScore") AS avg_quality_score
                FROM 
                    "Performance" p
                JOIN "Tasks" t ON t."taskId" = p."TaskID"
                WHERE 
                    t."ProjectID" = %s
                    AND p."UserID" = %s
                GROUP BY 
                    t."typeOfTask"
            """
            cursor.execute(query, (str(ProjectID), str(UserID)))  # convert UUID to string
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            conn.close()

            # Convert the query result into a dictionary with task types as keys and avg_quality_score as values
            result = {row[0]: row[1] for row in rows}  # Use indices to access the values (0 for task type, 1 for avg_quality_score)
            return result

        except Exception as e:
            print("Error fetching avg quality score per task type:", e)
            conn.close()
            return {"message": f"Error: {str(e)}"}
    return {"message": "Database connection failed."}




def get_users_in_project(project_id: UUID):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT "UserID"
                FROM "ProjectMembers"
                WHERE "ProjectID" = %s
            """
            cursor.execute(query, (str(project_id),))
            result = cursor.fetchall()
            conn.close()
            return {row[0] for row in result}  # return as set for fast lookup
        except Exception as e:
            print("Error fetching project members:", e)
            conn.close()
            return set()
    return set()

from .database import load_csv, save_csv

def fetch_successful_tasks():
    """ Fetch past successful tasks (quality_score ≥ 0.8) from CSV """
    df = load_csv("data/task_history.csv")
    # if df is not None:
    #     return df[df["quality_score"] >= 0.80][["user_id", "quality_score", "type_of_task", "priority_level"]]
    return df.to_dict(orient="records") if df is not None else []

def fetch_past_tasks():
    """ Fetch all users from CSV """
    df = load_csv("data/th.csv")
    return df.to_dict(orient="records") if df is not None else []

def fetch_unassigned_tasks():
    """Fetch all unassigned tasks by comparing tasks.csv with task_history.csv."""
    
    # Load tasks.csv (contains all tasks that can be assigned)
    tasks_df = pd.read_csv("data/tasks.csv")

    # Load task_history.csv (contains already assigned tasks)
    try:
        task_history_df = pd.read_csv("data/th.csv")
    except FileNotFoundError:
        task_history_df = pd.DataFrame(columns=["task_id"])  # Create an empty dataframe if file doesn't exist

    # Get the set of already assigned task IDs
    assigned_task_ids = set(task_history_df["task_id"]) if not task_history_df.empty else set()

    # Filter out tasks that have already been assigned
    unassigned_tasks_df = tasks_df[~tasks_df["task_id"].isin(assigned_task_ids)]

    return unassigned_tasks_df.to_dict(orient="records")  # Return as a list of dictionaries

def fetch_users_tasks():
    """ Fetch all users from CSV """
    df = pd.read_csv("data/th.csv")
    return df.to_dict(orient="records") if df is not None else []

def update_task_score(user_id, task_id, score):
    """ Update task quality score after task completion """
    df = pd.read_csv("data/th.csv")
    df.loc[(df["user_id"] == user_id) & (df["task_id"] == task_id), "quality_score"] = score
    save_csv(df, "data/th.csv")
    return {"message": "Task quality score updated."}


