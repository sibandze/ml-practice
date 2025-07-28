# Stochastic Gradient Descent (SGD) for Linear Regression

This directory explores Linear Regression trained using Stochastic Gradient Descent (SGD), showcasing both a custom implementation from scratch and an example using a popular machine learning library.

## Implementations

* **[From Scratch](#from-scratch-implementation)**: `linear_regression_sgd_from_scratch.py`
* **[Out-of-Box Library](#out-of-box-implementation)**: `linear_regression_sgd_from_oob.py`

---

## From Scratch Implementation

**File:** `linear_regression_sgd_from_scratch.py`

This project provides a fundamental understanding of how linear regression works by implementing the model and its training algorithm (Stochastic Gradient Descent) from first principles, without relying on high-level machine learning libraries like scikit-learn. It's designed to be clear, well-commented, and easy to follow for anyone interested in the mathematical and algorithmic underpinnings of machine learning.

### Features

* **Custom Linear Regression Model:** Implements the core linear equation $\hat{y} = Xw + b$.
* **Stochastic Gradient Descent (SGD):** Trains the model by updating weights and bias based on individual samples.
* **Cost Tracking:** Monitors the average cost (Mean Squared Error) per epoch to observe learning progress.
* **Data Shuffling:** Ensures proper stochasticity during training by shuffling data each epoch.
* **Minimal Dependencies:** Built primarily using NumPy for numerical operations.

### How it Works

The `LinearRegressionScratch` class encapsulates the linear regression model and its training logic using Stochastic Gradient Descent.

* **`__init__(self, learning_rate=0.01, n_iterations=1000)`**:
    * **Purpose:** Initializes the model's hyperparameters and internal state.
    * `learning_rate` (default: 0.01): Controls the step size of parameter updates during training.
    * `n_iterations` (default: 1000): Represents the number of "epochs" (full passes through the dataset) for training.
    * `weights`: The coefficients for each input feature, initialized to `None` and set to zeros during `fit_sgd`.
    * `bias`: The intercept term, initialized to `None` and set to zero during `fit_sgd`.
    * `costs`: A list to store the average cost (Mean Squared Error) at the end of each training epoch.

* **`fit_sgd(self, X, y)`**:
    * **Purpose:** Trains the linear regression model using Stochastic Gradient Descent.
    * **Input:**
        * `X` (numpy array): Input features (m samples, n features).
        * `y` (numpy array): Target values (m samples,).
    * **Process:**
        1.  **Parameter Initialization:** `self.weights` and `self.bias` are initialized to zeros.
        2.  **Epoch Loop:** Iterates for `n_iterations` (epochs).
        3.  **Data Shuffling:** For each epoch, the training data (`X` and `y`) is randomly shuffled to ensure proper stochasticity and prevent the model from getting stuck in local minima.
        4.  **Sample-wise Iteration:** The inner loop iterates through *each individual sample* in the shuffled dataset.
        5.  **Prediction:** For each sample $(x_i, y_i)$, a prediction $\hat{y}_i$ is made: $\hat{y}_i = x_i \cdot \text{weights} + \text{bias}$.
        6.  **Error Calculation:** The error for the single sample is calculated: $error_i = \hat{y}_i - y_i$.
        7.  **Gradient Calculation:** Gradients for weights ($dw_i$) and bias ($db_i$) are computed based on this single sample's error.
            * $dw_i = error_i \cdot x_i$
            * $db_i = error_i$
        8.  **Parameter Update:** The weights and bias are updated *immediately* after processing each sample using the learning rate:
            * $\text{weights} \leftarrow \text{weights} - \text{learning\_rate} \cdot dw_i$
            * $\text{bias} \leftarrow \text{bias} - \text{learning\_rate} \cdot db_i$
        9.  **Cost Accumulation:** The squared error for the current sample is added to an epoch's total cost.
        10. **Epoch Average Cost:** After all samples in an epoch are processed, the total cost is averaged and stored in `self.costs`.
        11. **Progress Output:** Periodically prints the current epoch's average cost.

* **`predict(self, X)`**:
    * **Purpose:** Makes predictions using the trained model.
    * **Input:** `X` (numpy array): Input features for which to make predictions.
    * **Output:** `np.ndarray`: Predicted target values using the learned weights and bias: $\hat{y} = X \cdot \text{weights} + \text{bias}$.

### Stochastic Gradient Descent (SGD) Explained

SGD is an optimization algorithm used to train machine learning models. It differs from Batch Gradient Descent (BGD) primarily in how it calculates and applies gradient updates:

* **Batch Gradient Descent (BGD):**
    * Calculates the gradient of the cost function using *all* training samples in each iteration.
    * Updates parameters (weights and bias) only *once per iteration* after considering the entire dataset.
    * Provides a precise gradient estimate, leading to smoother convergence.
    * Can be computationally expensive and slow for very large datasets due to processing all samples at once.

* **Stochastic Gradient Descent (SGD):**
    * Calculates the gradient and updates parameters using *only one randomly chosen training sample* at a time.
    * Updates parameters *after processing each individual sample*.
    * **Advantages:**
        * **Faster for large datasets:** Updates are frequent and computationally cheaper per update.
        * **Can escape local minima:** The "noisy" updates from single samples can help the optimization process avoid getting stuck in shallow local minima.
        * **Lower memory requirements:** Only one sample needs to be in memory for each update.
    * **Disadvantages:**
        * **Noisy updates:** The cost function might fluctuate significantly, leading to a less smooth convergence path.
        * **Requires careful learning rate tuning:** The noise can make finding an optimal learning rate more challenging.


