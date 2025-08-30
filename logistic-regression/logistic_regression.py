from scipy.special import expit
import numpy as np

class LogisticRegressionSGD_Scratch:
    def __init__(self, learning_rate=0.01, n_iterations=1000): 
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
        self.costs = [] # To store cost at each epoch

    def _binary_cross_entropy_cost(self, y_true, y_pred):
        """Calculates the binary cross-entropy cost for a single sample."""
        # Clip predictions to avoid log(0) or log(1)
        epsilon = 1e-15
        y_pred_clipped = np.clip(y_pred, epsilon, 1 - epsilon)
        return -(y_true * np.log(y_pred_clipped) + (1 - y_true) * np.log(1 - y_pred_clipped))

    def fit_sgd(self, X, y):
        '''
        Trains the logistic regression model using Stochastic Gradient Descent.

        Args:
            X (np.ndarray): Input features (m samples, n features).
            y (np.ndarray): Target values (m samples,).
        '''
        n_samples, n_features = X.shape

        # Initialize weights and bias
        self.weights = np.zeros(n_features)
        self.bias = 0
        self.costs = [] # Clear previous costs if refitting

        # Outer loop for epochs (one full pass through the dataset)
        for epoch in range(self.n_iterations):
            # Shuffle the data for each epoch to ensure stochasticity
            indices = np.arange(n_samples)
            np.random.shuffle(indices)
            X_shuffled = X[indices]
            y_shuffled = y[indices]

            epoch_total_cost = 0 # To accumulate cost for the current epoch

            # Inner loop: Iterate through each single sample (Stochastic part)
            for i in range(n_samples):
                x_i = X_shuffled[i] # Get a single sample's features
                y_i = y_shuffled[i] # Get a single sample's target

                # --- Forward Pass for a single sample ---
                z_i = np.dot(x_i, self.weights) + self.bias
                y_predicted_i = expit(z_i) # Sigmoid activation

                # --- Calculate Cost for this sample ---
                cost_i = self._binary_cross_entropy_cost(y_i, y_predicted_i)
                epoch_total_cost += cost_i

                # --- Backward Pass (Gradient Calculation for a single sample) ---
                # Gradient of BCE loss wrt weights: (y_pred - y_true) * x_i
                # Gradient of BCE loss wrt bias: (y_pred - y_true)
                error_i = y_predicted_i - y_i
                dw_i = error_i * x_i
                db_i = error_i

                # --- Update Weights and Bias ---
                self.weights += self.learning_rate * dw_i
                self.bias += self.learning_rate * db_i

            # --- End of Epoch ---
            # Calculate average cost for the epoch
            epoch_avg_cost = epoch_total_cost / n_samples
            self.costs.append(epoch_avg_cost)

            # Print progress periodically
            if (epoch % (self.n_iterations // 10) == 0 or epoch == self.n_iterations - 1):
                print(f"Epoch {epoch}/{self.n_iterations}: Cost = {epoch_avg_cost:.4f}")

    def predict(self, X):
        """
        Makes predictions using the trained model.

        Args:
            X (np.ndarray): Input features for prediction (m samples, n features).

        Returns:
            np.ndarray: Predicted target values (0 or 1) for each sample.
        """
        # Calculate the linear combination (z) for all samples in X
        z = np.dot(X, self.weights) + self.bias
        # Apply sigmoid to get probabilities
        y_probabilities = expit(z)
        # Apply the threshold (0.5) to get class predictions
        y_predicted_classes = (y_probabilities >= 0.5).astype(int)
        return y_predicted_classes
