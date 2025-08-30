import numpy as np

class LinearRegressionNormalEquations:
        def __init__(self):
                self.weights = None

        def fit(self, X, y):
                self.weights = np.linalg.pinv(X.T @ X) @ X.T @ y
                return True

        def predict(self, X):
                return np.dot(X, self.weights)
