import pandas as pd
from db.queries import fetch_task_performance, fetch_successful_tasks

# past_tasks = fetch_task_performance(ProjectID="3e0cf46a-af2f-4e0e-922e-d7144983e859")
past_tasks = fetch_successful_tasks()

# Convert to DataFrame if it's a list
if isinstance(past_tasks, list):
    if not past_tasks:
        print("message:No successful tasks found for comparison.")
    past_tasks = pd.DataFrame(past_tasks)
elif past_tasks.empty:
    print("message: Past task is empty")

# Compute avg_quality_score & task_count
summary = past_tasks.groupby(["workload", "type_of_task", "priority_level"]).agg(
    avg_quality_score=("quality_score", "mean"),
    task_count=("quality_score", "count")
).reset_index()

# Round the average quality score for cleaner output
summary["avg_quality_score"] = summary["avg_quality_score"].round(2)

# Print the results
for _, row in summary.iterrows():
    print(f"User: {row['workload']} | Task Type: {row['type_of_task']} | "
          f"Avg Quality Score: {row['avg_quality_score']} | Priority Lvl: {row['priority_level']} | Completed: {row['task_count']} times")
