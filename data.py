import pandas as pd
import uuid
import random
from datetime import datetime, timedelta

# Define task types
task_types = [
    "3D Model", "3D Render", "Conceptual Design", "Construction Document",
    "Custom Millwork & Joinery Drawing", "Design Development", "Door & Window Schedule",
    "Elevation Drawing", "Finish Schedule", "Floor Plan", "Furniture Layout Plan",
    "General Specification", "Hardscape Plan", "Interior Layout Plan", "Landscape Plan",
    "Lighting & Fixture Plan", "Material Board", "Partition Plan", "Permit Drawing",
    "Reflected Ceiling Plan", "Roof Plan", "Schematic Design", "Section Drawing",
    "Site Plan", "Technical Specification", "Virtual Reality", "Zoning & Building Code Compliance",
    "Others"
]

# Define realistic architectural tasks
task_templates = [
    ("3D Model Development", "Create a detailed 3D model for the client’s new residential project."),
    ("Render Finalization", "Enhance the 3D renders for the commercial building's presentation."),
    ("Conceptual Design Drafting", "Prepare an initial concept sketch for the urban park renovation."),
    ("Construction Documentation", "Compile detailed construction drawings for city permit approval."),
    ("Custom Joinery Design", "Develop detailed joinery drawings for the interior fit-out project."),
    ("Facade Elevation Detailing", "Finalize the detailed elevation drawings for the high-rise building."),
    ("Interior Layout Planning", "Optimize space planning for the luxury apartment interior."),
    ("Lighting Plan Design", "Create a lighting and fixture layout for the retail store."),
    ("Material Selection & Specification", "Curate materials and finishes for the sustainable home project."),
    ("Site Plan Drafting", "Prepare a site plan layout considering zoning and access."),
    ("Structural Coordination", "Coordinate with the structural engineer for beam placements."),
    ("Permit Drawing Submission", "Prepare and submit permit drawings for approval."),
    ("Landscape Design Refinement", "Enhance the planting layout for the residential garden."),
    ("Technical Specifications", "Compile technical specifications for the construction phase."),
    ("Hardscape Design Execution", "Design outdoor paving and seating areas for the commercial plaza.")
]

priority_levels = ["Low", "Neutral", "High"]

# Generate tasks.csv (400 tasks)
tasks_data = []
for _ in range(400):
    task_id = str(uuid.uuid4())
    title, description = random.choice(task_templates)
    type_of_task = random.choice(task_types)
    priority_level = random.choice(priority_levels)
    due_date = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")

    tasks_data.append([task_id, title, description, type_of_task, priority_level, due_date])

tasks_df = pd.DataFrame(tasks_data, columns=["task_id", "title", "description", "type_of_task", "priority_level", "due_date"])

# Generate tasks_history.csv (400 completed tasks from 10 users)
users = [str(uuid.uuid4()) for _ in range(10)]
user_names = [f"User {_+1}" for _ in range(10)]

# Sample completed tasks from tasks_df
tasks_history_data = []
sampled_tasks = tasks_df.sample(n=400, replace=False).copy()  # Ensure no duplication

for index, row in sampled_tasks.iterrows():
    user_index = random.randint(0, 9)
    user_id = users[user_index]
    name = user_names[user_index]
    quality_score = round(random.uniform(0.6, 1.00), 2)  # Higher quality scores to reflect skilled users
    
    # Add user details to the task history
    tasks_history_data.append([
        user_id, name, quality_score, 
        row["task_id"]
    ])

tasks_history_df = pd.DataFrame(tasks_history_data, columns=[
    "user_id", "name", "quality_score", "task_id"
])

# Save files
tasks_file_path = "data/tasks.csv"
tasks_history_file_path = "data/tasks_history.csv"

tasks_df.to_csv(tasks_file_path, index=False)
tasks_history_df.to_csv(tasks_history_file_path, index=False)

tasks_file_path, tasks_history_file_path
