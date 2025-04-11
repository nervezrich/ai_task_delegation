# train.py
import os
from data_preprocessing import load_data, preprocess_data
from model import tune_model, evaluate_model, learning_curve_plot
from sklearn.model_selection import train_test_split
import joblib

def train_model():
    # Load and preprocess data
    data_file = 'data/task_user_pairs.csv'
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Dataset file not found at {data_file}")

    df = load_data(data_file)
    X, y, pipeline = preprocess_data(df)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Building and tuning the model...")
    model = tune_model(X_train, y_train)

    # Save the model and pipeline
    joblib.dump(model, 'ml/task_delegation_model.pkl')
    joblib.dump(pipeline, 'ml/preprocessing_pipeline.pkl')
    print("Model and preprocessing pipeline saved.")

    print("Evaluating the model...")
    evaluate_model(model, X_test, y_test)

    print("Plotting learning curve...")
    learning_curve_plot(model, X_train, y_train)


if __name__ == "__main__":
    train_model()