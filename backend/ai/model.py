# model.py
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, mean_absolute_percentage_error
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np

def build_model():
    return MLPRegressor(hidden_layer_sizes=(100,), max_iter=1000, random_state=42)

def tune_model(X_train, y_train):
    param_grid = {
        'hidden_layer_sizes': [(50,), (100,), (200,)],
        'activation': ['relu', 'tanh'],
        'solver': ['adam', 'sgd'],
        'learning_rate': ['constant', 'adaptive'],
    }

    model = build_model()
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='neg_mean_absolute_error', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print(f"Best hyperparameters: {grid_search.best_params_}")
    return grid_search.best_estimator_

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)

    print(f"Mean Absolute Error (MAE): {mean_absolute_error(y_test, y_pred)}")
    print(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred)}")
    print(f"Root Mean Squared Error (RMSE): {np.sqrt(mean_squared_error(y_test, y_pred))}")
    print(f"R-squared (R²): {r2_score(y_test, y_pred)}")
    print(f"Mean Absolute Percentage Error (MAPE): {mean_absolute_percentage_error(y_test, y_pred)}")

    return y_pred

def learning_curve_plot(model, X_train, y_train):
    train_sizes, train_scores, test_scores = learning_curve(
        model, X_train, y_train, cv=5, scoring='neg_mean_absolute_error')

    plt.plot(train_sizes, -train_scores.mean(axis=1), label="Training Score")
    plt.plot(train_sizes, -test_scores.mean(axis=1), label="Cross-validation Score")
    plt.xlabel("Training Size")
    plt.ylabel("MAE")
    plt.title("Learning Curve")
    plt.legend()
    plt.show()
