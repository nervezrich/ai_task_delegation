import pandas as pd

# Load the task history CSV
tasks_history_df = pd.read_csv("data/th.csv")

# Group by user name and type_of_task to get average score and count
summary = tasks_history_df.groupby(["name", "type_of_task"]).agg(
    avg_quality_score=("quality_score", "mean"),
    task_count=("type_of_task", "count")
).reset_index()

# Round the average quality score for cleaner output
summary["avg_quality_score"] = summary["avg_quality_score"].round(2)

# Print the results
for _, row in summary.iterrows():
    print(f"User: {row['name']} | Task Type: {row['type_of_task']} | "
          f"Avg Quality Score: {row['avg_quality_score']} | Completed: {row['task_count']} times")
