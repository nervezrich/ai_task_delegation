# data_preprocessing.py
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

def load_data(file_path):
    return pd.read_csv(file_path)

def preprocess_data(df):
    X = df.drop(columns=["match_score"])
    y = df["match_score"]

    categorical_features = ["title", "description", "type_of_task", "priority_level", "preferred_task"]
    numeric_features = ["workload", "avg_quality_score"]

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    pipeline = Pipeline(steps=[('preprocessor', preprocessor)])
    X_processed = pipeline.fit_transform(X)

    return X_processed, y, pipeline