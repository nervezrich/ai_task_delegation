from models.cbf_model import assign_task
from db.queries import fetch_successful_tasks

def retrain_model():
    """ Retrains the AI model by updating user-task similarities """
    past_tasks = fetch_successful_tasks()
    if past_tasks.empty:
        return {"message": "No data available for retraining."}

    # **Recompute recommendations for all new tasks**
    updated_recommendations = [assign_task(task) for task in past_tasks.to_dict(orient="records")]
    
    return {"message": "Model retrained successfully.", "updated_recommendations": updated_recommendations}
