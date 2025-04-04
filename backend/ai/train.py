from models.cbf_model import assign_task
from db.queries import fetch_past_tasks

def retrain_model():
    """ Retrains the AI model by updating user-task similarities """
    past_tasks = fetch_past_tasks()
    
    # Check if the past_tasks list is empty
    if not past_tasks:
        return {"message": "No data available for retraining."}

    # Pass the entire list of tasks at once to assign_task
    updated_recommendations = assign_task(past_tasks)
    
    return {"message": "Model retrained successfully.", "updated_recommendations": updated_recommendations}
