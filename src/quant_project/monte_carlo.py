import numpy as np

# Simulation parameters
S_0 = 1.20  # Spot price in dollars
r = 0.02  # Risk-free rate (2%)
sigma = 0.25  # Volatility (25%)
T = 0.5  # Time to maturity in years
num_simulations = 10000  # Number of simulations
num_steps = 252  # Number of steps (daily)

# Time increment
dt = T / num_steps

# Simulating price paths
np.random.seed(42)  # For reproducibility
price_paths = np.zeros((num_steps, num_simulations))
price_paths[0] = S_0

for t in range(1, num_steps):
    z = np.random.standard_normal(num_simulations)
    price_paths[t] = price_paths[t-1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

# Calculating the average simulated price at maturity
average_simulated_price = np.mean(price_paths[-1])
print(f"Average monte carlo simulated price at maturity: {average_simulated_price:.4f}")