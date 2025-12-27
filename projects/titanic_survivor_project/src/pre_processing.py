import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import os 

# --- Configuration ---
# Define the columns that will be used for the model AFTER feature engineering
COLUMNS_FOR_MODEL = [
    'Survived',
    'Pclass',
    'Sex',
    'Age',
    'SibSp',
    'Parch',
    'Fare',
    'Embarked',
    'HasCabin'  # The engineered feature
]
TARGET_COLUMN = 'Survived'


def load_data(filepath):
    """
    Loads the raw Titanic dataset from a specified filepath.
    """
    print(f"Loading data from {filepath}...")
    try:
        df = pd.read_csv(filepath)
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None


def save_processed_data(df, output_filepath):
    """
    Saves the processed DataFrame (before train/test split) to a CSV file.
    """
    print(f"Saving processed data to {output_filepath}...")
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    df.to_csv(output_filepath, index=False)
    print("Processed data saved.")


def impute_missing_values(df):
    """
    Imputes missing 'Age' and 'Embarked' values.

    - 'Age' is imputed using the median Age grouped by 'Pclass' and 'Sex'.
    - 'Embarked' is imputed using the mode (most frequent value).
    """
    # Use a copy to avoid SettingWithCopyWarning if a slice was passed
    df_imputed = df.copy()

    # --- Age Imputation (Grouped Median) ---
    df_imputed['Age'] = df_imputed.groupby(['Pclass', 'Sex'])['Age'].transform(lambda x: x.fillna(x.median()))

    # --- Embarked Imputation (Mode) ---
    mode_embarked = df_imputed['Embarked'].mode()[0]
    df_imputed.fillna({'Embarked': mode_embarked}, inplace=True)

    # Fill missing Fare
    df_imputed.fillna({
                      'Fare': df_imputed['Fare'].median()
                      },
                      inplace=True)

    print("Imputation complete (Age, Embarked, Fare handled).")
    return df_imputed


def create_cabin_feature(df):
    """
    Creates a binary feature 'HasCabin' from the 'Cabin' column.
    """
    # Checks if 'Cabin' is NOT NaN and converts boolean to integer (1 or 0)
    df['HasCabin'] = df['Cabin'].notna().astype(int)
    print("Created 'HasCabin' feature.")
    return df


def preprocess_data(df):
    """
    Applies final processing: selects columns and performs one-hot encoding.
    """

    # 1. Selects relevant columns
    df_transformed = df[COLUMNS_FOR_MODEL].copy()

    # 2. One-hot encode categorical features
    # 'Pclass' is treated as categorical for encoding
    categorical_cols = ['Sex', 'Embarked', 'Pclass']
    df_transformed = pd.get_dummies(df_transformed, columns=categorical_cols, drop_first=True)

    return df_transformed


def split_data(df_transformed, test_size=0.2, random_state=268, target_column=TARGET_COLUMN):
    """
    Separates the target (y) and features (X) and splits the data.
    """
    # Separate target variable (y) and features (X)
    X = df_transformed.drop(target_column, axis=1)
    y = df_transformed[target_column]

    print(f"Splitting data into train ({1-test_size:.0%} | test {test_size:.0%})...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
    return X, y, X_train, X_test, y_train, y_test


def reprocess_and_split_data(raw_data_path, processed_data_path, split_ratio=0.2):
    """
    The main orchestration method.
    It loads, cleans, engineers features, saves the processed dataset,
    and finally splits the data into X, y, X_train, etc.

    Returns:
        X (pd.DataFrame): All features.
        y (pd.Series): Target variable.
        X_train (pd.DataFrame): Training features.
        X_test (pd.DataFrame): Testing features.
        y_train (pd.Series): Training target.
        y_test (pd.Series): Testing target.
    """
    print("\n--- Starting Data Reprocessing Pipeline ---")

    # 1. Load Data
    df_raw = load_data(raw_data_path)
    if df_raw is None:
        return None, None, None, None, None, None

    # 2. Impute Missing Values
    df_imputed = impute_missing_values(df_raw)

    # 3. Feature Engineering (HasCabin)
    df_featured = create_cabin_feature(df_imputed)

    # 4. Final Processing and Encoding (This is the pre-split DataFrame)
    df_transformed = preprocess_data(df_featured)

    # 5. Save Processed Data to CSV (as requested)
    save_processed_data(df_transformed, processed_data_path)

    # 6. Split Data
    X, y, X_train, X_test, y_train, y_test = split_data(df_transformed, test_size=split_ratio)

    print("--- Pipeline Finished ---")

    # Return the processed datasets (all X, y, and the split versions)
    return X, y, X_train, X_test, y_train, y_test


# Add an __main__ block for basic function testing if run directly
if __name__ == '__main__':
    print("Testing reprocess_and_split_data structure...")
    # NOTE: You must provide a valid path for this to run in a non-Colab environment
    # Example placeholder paths relative to the project root:
    RAW_PATH = '../data/raw/titanic.csv' 
    PROCESSED_PATH = '../data/processed/titanic_processed.csv'
    try:
         X, y, X_train, X_test, y_train, y_test = reprocess_and_split_data(RAW_PATH, PROCESSED_PATH)
         if X is not None:
             print(f"Test Successful. Final X shape: {X.shape}")
    except Exception as e:
         print(f"Test Failed: {e}")
