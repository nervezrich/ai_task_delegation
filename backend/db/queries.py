from .database import get_db_connection
import pandas as pd

def fetch_past_tasks(ProjectID):
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
            cursor.execute(query, (ProjectID,))
            result = cursor.fetchall()
            conn.close()
            return pd.DataFrame(result)
        except Exception as e:
            print("Error fetching past tasks:", e)
            conn.close()
            return []
    return []


print(fetch_past_tasks("3e0cf46a-af2f-4e0e-922e-d7144983e859"))


from .database import load_csv, save_csv

def fetch_successful_tasks():
    """ Fetch past successful tasks (quality_score ≥ 0.8) from CSV """
    df = load_csv("data/th.csv")
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


