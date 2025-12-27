import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report

def get_candidate_models():
    """
    Defines the models and hyperparameter grids to be tuned.
    Returns a dictionary where keys are model names and values are 
    dictionaries containing the 'model' instance and 'params' grid.
    """
    model_configs = {
        'LogisticRegression': {
            'model': LogisticRegression(random_state=268, max_iter=1000),
            'params': {
                'solver': ['liblinear', 'lbfgs'],
                'C': [0.01, 0.1, 1, 10, 100],
                'l1_ratio': [0] # l2 works for both solvers
            }
        },
        'RandomForest': {
            'model': RandomForestClassifier(random_state=268),
            'params': {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 5, 10, 20],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4]
            }
        }
    }
    return model_configs

def train_and_tune_models(X_train, y_train, model_configs):
    """
    Iterates through model configs, performs GridSearchCV for each,
    and stores the best estimator and results.
    """
    results = {}

    print("--- Starting Hyperparameter Tuning (CV=5) ---")

    for model_name, config in model_configs.items():
        print(f"Tuning {model_name}...")
        model = config['model']
        params = config['params']

        # Initialize GridSearchCV
        # cv=5 means 5-fold Cross-Validation
        # n_jobs=-1 uses all available processor cores
        grid_search = GridSearchCV(
            estimator=model,
            param_grid=params,
            cv=5,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )

        grid_search.fit(X_train, y_train)

        results[model_name] = {
            'best_model': grid_search.best_estimator_,
            'best_params': grid_search.best_params_,
            'best_cv_score': grid_search.best_score_
        }

        print(f"  Best CV Score: {grid_search.best_score_:.4f}")
        print(f"  Best Params: {grid_search.best_params_}")

    return results

def select_best_model(results):
    """
    Compares tuned models based on their Best CV Score and returns the winner.
    """
    best_model_name = None
    best_model_object = None
    highest_score = 0

    print("\n--- Selecting Best Model ---")

    for name, result in results.items():
        score = result['best_cv_score']
        if score > highest_score:
            highest_score = score
            best_model_name = name
            best_model_object = result['best_model']

    print(f"🏆 Winner: {best_model_name} with CV Accuracy: {highest_score:.4f}")
    return best_model_object, best_model_name

def evaluate_model(model, X_test, y_test):
    """
    Runs the final evaluation on the unseen Test set.
    """
    print(f"\n--- Final Evaluation on Test Set ---")
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)

    print(f"Test Accuracy: {acc:.4f}")
    print("Classification Report:")
    print(report)
    return acc

def save_model(model, filepath):
    """
    Saves the trained model to disk using joblib.
    """
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")
