import numpy as np

class LocallyWeightedLinearRegressionSGD:
	def __init__(self, tau = 1, learning_rate = 0.01, n_iterations = 1000):
		self.tau = tau
		self.learning_rate = learning_rate
		self.n_iterations = n_iterations
		self.weights = None

	def _calcalate_local_weights(self, X, x_query):
		dist = np.linalg.norm(X - x_query, axis = 1)
		weights = np.exp(-dist**2 / (2 * self.tau**2))
		return np.diag(weights)


	def fit(self, X, y, x_query):
		local_weights = self._calcalate_local_weights(X, x_query)
		self.weights = np.zeros(X.shape[1])
		for _ in range(self.n_iterations):
			for i in range(X.shape[0]):
				y_hat = np.dot(X[i], self.weights)
				error = y_hat - y[i]
				self.weights -= learning_rate * local_weight[i,i] * error * X[i]
		return True

        def predict(self, X):
                return np.dot(X, self.weights)
