# train_model.py

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

# Load task history CSV
df = pd.read_csv("data/th.csv")

# Aggregate past performance
summary = df.groupby(["name", "type_of_task", "priority_level"]).agg(
    avg_quality_score=("quality_score", "mean"),
    task_count=("type_of_task", "count")
).reset_index()

# Merge back into main DataFrame
df = pd.merge(df, summary, on=["name", "type_of_task", "priority_level"], how="left")

# One-hot encode
encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(df[["type_of_task", "priority_level"]])
joblib.dump(encoder, "backend/models/encoder.joblib")

# Normalize numerical features
scaler = StandardScaler()
numerical = scaler.fit_transform(df[["avg_quality_score", "task_count"]])
joblib.dump(scaler, "backend/models/scaler.joblib")

# Labels
user_ids = df["user_id"].unique()
user_map = {uid: i for i, uid in enumerate(user_ids)}
reverse_map = {i: uid for uid, i in user_map.items()}
df["label"] = df["user_id"].map(user_map)
joblib.dump(reverse_map, "backend/models/user_id_reverse_map.joblib")

# Feature matrix
X = np.hstack([encoded, numerical])
y = df["label"].values

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
joblib.dump(model, "backend/models/random_forest_task_assigner.joblib")

# Accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {acc * 100:.2f}%")
