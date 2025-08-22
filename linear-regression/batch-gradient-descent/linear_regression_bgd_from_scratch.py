import numpy as np

class LinearRegressionBGD_Scratch:
	def __init__(self, learning_rate = 0.01, n_iterations = 1000):
		self.learning_rate = learning_rate
		self.n_iterations = n_iterations
		self.weights = None
		self.bias = None
		self.costs = []

	def fit(self, X, y):
		"""
		Trains the linear regression model using gradiet descent.

		Args:
			X (np.array): Input features (m samples, n features).
			y (np.array): Target values (m samples).
		"""
		n_samples, n_features = X.shape

		# Initialize weights and bias to zeros
		self.weights = np.zeros(n_features)
		self.bias = 0

		# Gradient Descent loop
		for i in range(self.n_iterations):
			# Predict y_hat
			y_predicted = np.dot(X, self.weights) + self.bias

			# Calculate the cost (MSE) and store it
			cost =  (1/(2*n_samples)) * np.sum((y_predicted - y)**2)
			self.costs.append(cost)

			# Calculate gradients
			# (y_predicted - y) is the error/difference
			dw = (1/n_samples) * np.dot(X.T, (y_predicted - y))
			db = (1/n_samples) * np.sum(y_predicted - y)

			# Update weights and bias
			self.weights -= self.learning_rate*dw
			self.bias -= self.learning_rate*db

			if i % (self.n_iterations // 10)  == 0:
				print(f"Iteration {i}: Cost = {cost:.4f}")

	def predict(self, X):
		"""
		Makes predictions using the trained model.

		Args:
			 X (np.ndarray): Input features for prediction.

			Returns:
				np.ndarray: Predicted target values.
		"""
		return np.dot(X, self.weights) + self.bias
