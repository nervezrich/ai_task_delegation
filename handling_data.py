import pandas as pd
from backend.db.queries import fetch_users_tasks

# Load the task history CSV
successful_tasks = fetch_users_tasks()

# Convert to DataFrame if it's a list
if isinstance(successful_tasks, list):
    if not successful_tasks:
        print({"message": "No successful tasks found for comparison."})
    successful_tasks = pd.DataFrame(successful_tasks)
elif successful_tasks.empty:
    print({"message": "No successful tasks found for comparison."})

# Group by user name and type_of_task to get average score and count
summary = successful_tasks.groupby(["name", "type_of_task", "priority_level"]).agg(
    avg_quality_score=("quality_score", "mean"),
    task_count=("type_of_task", "count"),
).reset_index()

# Round the average quality score for cleaner output
summary["avg_quality_score"] = summary["avg_quality_score"].round(2)

# Print the results
for _, row in summary.iterrows():
    print(f"User: {row['name']} | Task Type: {row['type_of_task']} | "
          f"Avg Quality Score: {row['avg_quality_score']} | Priority Lvl: {row['priority_level']} | Completed: {row['task_count']} times")
