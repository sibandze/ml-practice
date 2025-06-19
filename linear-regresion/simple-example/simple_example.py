import torch
import torch.nn as nn
import torch.optim as optim
# Generate synthetic data
X = torch.randn(100, 1) * 10 # 100 samples, 1 feature
y = 2 * X + 3 + torch.randn(100, 1) * 2 # y = 2x + 3 + noise

# Define the model
model = nn.Linear(1, 1) # Input size 1, output size 1
# Define the loss function
loss_fn = nn.MSELoss() # Mean Squared Error
# Define the optimizer
optimizer = optim.SGD(model.parameters(), lr=0.01) # Stochastic Gradient Descent
# Training loop
epochs = 1000
for epoch in range(epochs):
  # Forward pass  
  y_pred = model(X)
  loss = loss_fn(y_pred, y)
  
  # Backward pass and optimization  
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()

  if (epoch+1) % 100 == 0:
    print(f'Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}')
    
# Print learned parameters
print(f'w: {model.weight.item():.4f}, b: {model.bias.item():.4f}')
# Make predictions
x_test = torch.tensor([[5.0], [10.0]])
y_test_pred = model(x_test)
print(f'Predictions for x = 5 and x = 10: {y_test_pred.tolist()}')
