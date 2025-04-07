# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import OneHotEncoder, StandardScaler
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
# import joblib

# # Load task history CSV
# df = pd.read_csv("data/th.csv")

# # Group by user name, type_of_task, and priority_level to get average score and count
# summary = df.groupby(["name", "type_of_task", "priority_level"]).agg(
#     avg_quality_score=("quality_score", "mean"),
#     task_count=("type_of_task", "count")
# ).reset_index()

# # Merge this summary back to the original dataframe to get avg_quality_score and task_count for each row
# df = pd.merge(df, summary, on=["name", "type_of_task", "priority_level"], how="left")

# # One-hot encode categorical features (type_of_task and priority_level)
# encoder = OneHotEncoder(sparse_output=False)
# encoded_features = encoder.fit_transform(df[["type_of_task", "priority_level"]])

# # Save encoder for future inference
# joblib.dump(encoder, "backend/models/encoder.joblib")

# # Prepare labels (target is user_id)
# user_ids = df['user_id'].unique()
# user_id_map = {uid: idx for idx, uid in enumerate(user_ids)}
# user_id_reverse_map = {v: k for k, v in user_id_map.items()}

# y = df['user_id'].map(user_id_map).values

# # Normalize avg_quality_score and task_count
# scaler = StandardScaler()
# avg_quality_scaled = scaler.fit_transform(df[["avg_quality_score", "task_count"]])

# joblib.dump(scaler, "backend/models/scaler.joblib")

# # Final feature matrix (combine encoded features with avg_quality_score and task_count)
# X = np.hstack([encoded_features, avg_quality_scaled])

# # Train/test split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train a Random Forest model
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_train, y_train)

# # Save the trained model
# joblib.dump(model, "backend/models/random_forest_task_assigner.joblib")

# # Save reverse mapping for inference
# joblib.dump(user_id_reverse_map, "backend/models/user_id_reverse_map.joblib")

# # Evaluate the model
# y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(f"Model accuracy: {accuracy * 100:.2f}%")
