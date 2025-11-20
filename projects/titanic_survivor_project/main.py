import sys
import os
import pandas as pd

# Import modules
from src.data_processing import reprocess_and_split_data
from src.models import (
    get_candidate_models,
    train_and_tune_models,
    select_best_model,
    save_model
)
# Import the new evaluate functions
from src.evaluate import plot_confusion_matrix, plot_roc_curve, plot_feature_importance

# --- Configuration ---
BASE_PATH = './' # '/content/drive/MyDrive/ML/projects/titanic_survival_project'
RAW_DATA_PATH = os.path.join(BASE_PATH, 'data/raw/titanic.csv')
PROCESSED_DATA_PATH = os.path.join(BASE_PATH, 'data/processed/titanic_processed.csv')
MODEL_SAVE_PATH = os.path.join(BASE_PATH, 'models/titanic_best_model.pkl')
FIGURES_DIR = os.path.join(BASE_PATH, 'reports/figures')

SPLIT_RATIO = 0.2

def main():
    print("--- Titanic Survival Prediction Pipeline ---")

    # 1. Data Processing
    X, y, X_train, X_test, y_train, y_test = reprocess_and_split_data(
        raw_data_path=RAW_DATA_PATH,
        processed_data_path=PROCESSED_DATA_PATH,
        split_ratio=SPLIT_RATIO
    )

    if X is None:
        return

    # 2. Model Tuning & Selection
    model_configs = get_candidate_models()
    tuning_results = train_and_tune_models(X_train, y_train, model_configs)
    final_model, model_name = select_best_model(tuning_results)

    # 3. Save the Best Model
    save_model(final_model, MODEL_SAVE_PATH)

    # 4. Comprehensive Evaluation & Visualization
    print("\n--- Generating Evaluation Reports ---")

    # Generate Predictions for Confusion Matrix
    y_pred = final_model.predict(X_test)

    # A. Confusion Matrix
    cm_path = os.path.join(FIGURES_DIR, 'confusion_matrix.png')
    plot_confusion_matrix(y_test, y_pred, cm_path)

    # B. ROC Curve
    roc_path = os.path.join(FIGURES_DIR, 'roc_curve.png')
    plot_roc_curve(final_model, X_test, y_test, roc_path)

    # C. Feature Importance
    # We need feature names from the DataFrame (X_train)
    fi_path = os.path.join(FIGURES_DIR, 'feature_importance.png')
    plot_feature_importance(final_model, X_train.columns, fi_path)

    print("\nPipeline execution completed successfully. Check 'reports/figures/' for plots.")

if __name__ == "__main__":
    main()
