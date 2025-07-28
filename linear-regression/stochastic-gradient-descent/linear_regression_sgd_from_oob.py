import numpy as np
from sklearn.linear_model import SGDRegressor

class LinearRegressionSGD_OOB:
    """
    Linear Regression model using Scikit-learn's SGDRegressor,
    wrapped to mimic the API of LinearRegressionScratch for consistent usage.
    """
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        """
        Initializes the SGDRegressor with specified hyperparameters.

        Args:
            learning_rate (float): The learning rate (eta0 in SGDRegressor).
            n_iterations (int): The maximum number of passes over the training data (max_iter in SGDRegressor).
        """
        # SGDRegressor uses 'eta0' for learning rate and 'max_iter' for number of epochs
        self.model = SGDRegressor(eta0=learning_rate, max_iter=n_iterations, random_state=42)
        # We'll store coefficients and intercept after fitting for consistency,
        # though they are directly accessible via self.model.coef_ and self.model.intercept_
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        """
        Trains the linear regression model using Scikit-learn's SGDRegressor.

        Args:
            X (np.ndarray): Input features (m samples, n features).
            y (np.ndarray): Target values (m samples,).
        """
        # Scikit-learn models typically expect y to be 1D for regression
        if y.ndim > 1:
            y = y.flatten()

        self.model.fit(X, y)

        # Store the learned parameters for consistent access
        self.weights = self.model.coef_
        self.bias = self.model.intercept_
        
        print(f"OOB Model Fitted. Coefficients: {self.weights}, Intercept: {self.bias}")


    def predict(self, X):
        """
        Makes predictions using the trained Scikit-learn SGDRegressor model.

        Args:
            X (np.ndarray): Input features for prediction.

        Returns:
            np.ndarray: Predicted target values.
        """
        return self.model.predict(X)
