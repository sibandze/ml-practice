import numpy as np

class LinearRegressionSGD_Scratch:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
        self.costs = [] # To store cost at each iteration

    def fit_sgd(self, X, y):
        '''
        Trains the linear regression model using Stochastic Gradient Descent (LMS).

        Args:
            X (np.ndarray): Input features (m samples, n features).
            y (np.ndarray): Target values (m samples,).
        '''
        n_samples, n_features = X.shape

        # Initialize weights and bias to zeros
        self.weights = np.zeros(n_features)
        self.bias = 0

        # SGD Loop (n_iterations are now "epochs")
        for epoch in range(self.n_iterations): # Outer loop for epochs
            # Shuffle the data for each epoch to ensure stochasticity
            indices = np.arange(n_samples)
            np.random.shuffle(indices) # Shuffle the indices
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            epoch_total_cost = 0 # To calculate average cost for the current epoch

            # Inner loop: Iterate through each single sample
            for i in range(n_samples):
                x_i = X_shuffled[i] # Get a single sample's features
                y_i = y_shuffled[i] # Get a single sample's target

                # Predict y_hat for the *single sample*
                y_predicted_i = np.dot(x_i, self.weights) + self.bias

                # Calculate error for the single sample
                error_i = y_predicted_i - y_i

                # Calculate gradients for the *single sample* (no division by n_samples here)
                # Note: The '2' from the 1/2 in cost is implicitly handled by the derivative
                # For dw, it's error * x_i
                dw_i = error_i * x_i
                db_i = error_i # Gradient for bias is just the error

                # Update weights and bias *immediately after each sample*
                self.weights -= self.learning_rate * dw_i
                self.bias -= self.learning_rate * db_i

                # Accumulate cost for this sample to average later for the epoch
                # Cost for a single sample (not averaged yet)
                epoch_total_cost += (error_i**2) / 2 # Using the 1/2 from MSE for single sample

            # After processing all samples in the epoch, calculate and store the average cost
            epoch_avg_cost = epoch_total_cost / n_samples
            self.costs.append(epoch_avg_cost)

            if (epoch % (self.n_iterations // 10) == 0):
                print(f"Epoch {epoch}: Cost = {epoch_avg_cost:.4f}")

    def predict(self, X):
        """
        Makes predictions using the trained model.

        Args:
            X (np.ndarray): Input features for prediction.

        Returns:
            np.ndarray: Predicted target values.
        """
        return np.dot(X, self.weights) + self.bias
