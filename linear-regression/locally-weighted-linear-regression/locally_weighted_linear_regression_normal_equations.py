import numpy as np

class LocallyWeightedLinearRegressionNormalEquations:
	def __init__(self, tau):
		self.tau = tau

	def _calcalate_local_weights(self, X, x_query):
		dist = np.linalg.norm(X - x_query, axis = 1)
		weights = np.exp(-dist**2 / (2 * self.tau**2))
		return np.diag(weights)

	def fit_and_predict(self, X, y, X_query):
		predictions = []
		for x_query in X_query:
			local_weights = self._calculate_local_weights(X, x_query)
			weights = np.linalg.pinv(X.T @ local_weights @ X) @ X.T @ local_weights @ y
			prediction = np.dot(x_query, weights)
			predictions.append(prediction)
		return predictions 

   
