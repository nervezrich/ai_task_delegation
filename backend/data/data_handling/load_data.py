import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_task = pd.read_csv('https://raw.githubusercontent.com/nervezrich/ai_task_delegation/refs/heads/main/data/tasks.csv')
df_task_history = pd.read_csv('https://raw.githubusercontent.com/nervezrich/ai_task_delegation/refs/heads/main/data/tasks_history.csv')

task_data = pd.merge(df_task, df_task_history, on='task_id')

print(task_data.head())