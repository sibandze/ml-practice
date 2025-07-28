import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from linear_regression_sgd_from_scratch import LinearRegressionSGD_Scratch
from linear_regression_sgd_from_oob import LinearRegressionSGD_OOB

# --- 1. Generate some synthetic data ---
np.random.seed(42)
# Using more data points for a better visual representation and split
num_samples = 200
X_full = 2 * np.random.rand(num_samples, 1) # Full dataset features
y_full = 4 + 3 * X_full + np.random.randn(num_samples, 1) # Full dataset targets

# Ensure y_full is 1D
y_full = y_full.flatten()

# Split data into training and testing sets
# We'll use X_train and y_train for fitting
# We'll use X_test for evaluating predictions (unseen data)
X_train, X_test, y_train, y_test = train_test_split(X_full, y_full, test_size=0.2, random_state=42)

# Create a range of values for plotting the regression line over the data's domain
# This ensures the line extends across the scatter plot, not just specific prediction points
X_plot = np.linspace(X_full.min(), X_full.max(), 100).reshape(-1, 1)


# --- 2. Initialize and Train the From-Scratch Model ---
print("\n--- Training From-Scratch Model ---")
# Adjust iterations for potentially more complex convergence with larger data
scratch_model = LinearRegressionScratch(learning_rate=0.01, n_iterations=200) # Increased iterations
scratch_model.fit_sgd(X_train, y_train) # Fit on training data

print(f"\nScratch Model Learned Weights: {scratch_model.weights}")
print(f"Scratch Model Learned Bias: {scratch_model.bias}")

# Make predictions on the test set
predictions_scratch_test = scratch_model.predict(X_test)
mse_scratch = mean_squared_error(y_test, predictions_scratch_test)
print(f"Scratch Model MSE on Test Set: {mse_scratch:.4f}")

# Generate predictions for plotting the line
predictions_scratch_plot = scratch_model.predict(X_plot)


# --- 3. Initialize and Train the Out-of-Box Model ---
print("\n--- Training Out-of-Box Model (Scikit-learn SGDRegressor) ---")
# Ensure consistent iterations
oob_model = LinearRegressionSGD_OOB(learning_rate=0.01, n_iterations=200) # Increased iterations
oob_model.fit(X_train, y_train) # Fit on training data

print(f"\nOOB Model Learned Weights: {oob_model.weights}")
print(f"OOB Model Learned Bias: {oob_model.bias}")

# Make predictions on the test set
predictions_oob_test = oob_model.predict(X_test)
mse_oob = mean_squared_error(y_test, predictions_oob_test)
print(f"OOB Model MSE on Test Set: {mse_oob:.4f}")

# Generate predictions for plotting the line
predictions_oob_plot = oob_model.predict(X_plot)


# --- 4. Plotting Results ---

# Plot for From-Scratch Model
plt.figure(figsize=(14, 7)) # Slightly larger figure for better visibility
plt.subplot(1, 2, 1) # 1 row, 2 columns, 1st plot
plt.scatter(X_train, y_train, label='Training Data', alpha=0.6, s=20, color='lightgray') # Smaller, lighter training points
plt.scatter(X_test, y_test, label='Test Data', alpha=0.8, s=30, color='darkorange') # Clearly distinguish test points
plt.plot(X_plot, predictions_scratch_plot, "r-", linewidth=2, label='Scratch LR Line')
plt.xlabel("X")
plt.ylabel("y")
plt.title(f"Linear Regression (From Scratch SGD)\nTest MSE: {mse_scratch:.4f}")
plt.legend()
plt.grid(True)

# Plot for Out-of-Box Model
plt.subplot(1, 2, 2) # 1 row, 2 columns, 2nd plot
plt.scatter(X_train, y_train, label='Training Data', alpha=0.6, s=20, color='lightgray')
plt.scatter(X_test, y_test, label='Test Data', alpha=0.8, s=30, color='darkorange')
plt.plot(X_plot, predictions_oob_plot, "b-", linewidth=2, label='OOB LR Line')
plt.xlabel("X")
plt.ylabel("y")
plt.title(f"Linear Regression (Out-of-Box SGDRegressor)\nTest MSE: {mse_oob:.4f}")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Plot the cost history for the scratch model
plt.figure(figsize=(8, 5))
plt.plot(range(len(scratch_model.costs)), scratch_model.costs, marker='o', linestyle='-', color='purple')
plt.xlabel("Epoch")
plt.ylabel("Average Cost (MSE)")
plt.title("Cost History (From-Scratch SGD)")
plt.grid(True)
plt.show()

print("\n--- Comparison ---")
print(f"True Coefficients (approx): [3.0]") # Based on y = 4 + 3x + noise
print(f"True Intercept (approx): 4.0")
print(f"Scratch Model Weights: {scratch_model.weights}")
print(f"Scratch Model Bias: {scratch_model.bias}")
print(f"OOB Model Weights: {oob_model.weights}")
print(f"OOB Model Bias: {oob_model.bias}")
print(f"\nScratch Model Test MSE: {mse_scratch:.4f}")
print(f"OOB Model Test MSE: {mse_oob:.4f}")
print(f"\nPredictions for a small X_test sample:\n")
for i in range(min(5, len(X_test))): # Print first 5 test samples and their predictions
    print(f"X_test[{i}]: {X_test[i][0]:.2f}, True y: {y_test[i]:.2f}, "
          f"Scratch Pred: {predictions_scratch_test[i]:.2f}, OOB Pred: {predictions_oob_test[i]:.2f}")
