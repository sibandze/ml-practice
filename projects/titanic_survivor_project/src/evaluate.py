import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from sklearn.metrics import confusion_matrix, roc_curve, auc

def save_plot(figure, filepath):
    """Helper to save a matplotlib figure to a specific path."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    figure.savefig(filepath, bbox_inches='tight', dpi=300)
    print(f"Saved plot to {filepath}")
    plt.close(figure) # Close to free memory

def plot_confusion_matrix(y_true, y_pred, output_path):
    """
    Generates and saves a heatmap of the confusion matrix.
    """
    cm = confusion_matrix(y_true, y_pred)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm,
                annot=True,
                fmt='d',
                cmap='Blues',
                cbar=False,
                ax=ax)

    ax.set_title('Confusion Matrix')
    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_xticklabels(['Died', 'Survived'])
    ax.set_yticklabels(['Died', 'Survived'])

    save_plot(fig, output_path)

def plot_roc_curve(model, X_test, y_test, output_path):
    """
    Generates and saves the Receiver Operating Characteristic (ROC) curve.
    """
    # Get probabilities for the positive class (Survived = 1)
    if hasattr(model, "predict_proba"):
        y_probs = model.predict_proba(X_test)[:, 1]
    else:
        print("Model does not support probability predictions. Skipping ROC curve.")
        return

    fpr, tpr, thresholds = roc_curve(y_test, y_probs)
    roc_auc = auc(fpr, tpr)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(
            fpr,
            tpr,
            color='darkorange',
            lw=2,
            label=f'ROC curve (AUC = {roc_auc:.2f})'
           )
    ax.plot(
            [0, 1],
            [0, 1],
            color='navy',
            lw=2, linestyle='--'
           )

    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('Receiver Operating Characteristic (ROC)')
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)

    save_plot(fig, output_path)

def plot_feature_importance(model, feature_names, output_path):
    """
    Extracts and plots feature importance (for Trees) or Coefficients (for LogReg).
    """
    importances = None
    title = "Feature Importance"

    # 1. Check for Tree-based Feature Importances (Random Forest)
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        title = "Random Forest Feature Importance"

    # 2. Check for Linear Model Coefficients (Logistic Regression)
    elif hasattr(model, 'coef_'):
        importances = model.coef_[0]
        title = "Logistic Regression Coefficients"

    if importances is None:
        print("Model type not supported for feature importance plotting.")
        return

    # Create a DataFrame for easy plotting
    feature_df = pd.DataFrame({
        'Feature': feature_names,
        'Importance': importances
    })

    # For coefficients, we might care about magnitude (absolute value) for sorting
    # or raw values to see positive/negative correlation. 
    # Here we sort by absolute magnitude but plot raw values.
    feature_df['Abs_Importance'] = feature_df['Importance'].abs()
    feature_df = feature_df.sort_values(by='Abs_Importance', ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
                x='Importance',
                y='Feature',
                data=feature_df,
                palette='viridis',
                ax=ax
               )

    ax.set_title(title)
    ax.set_xlabel('Importance Score')
    ax.axvline(x=0, color='black', linestyle='-', linewidth=0.5) # Zero line for coefficients
    save_plot(fig, output_path)
