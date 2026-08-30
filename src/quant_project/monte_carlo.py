import numpy as np

def monte_carlo_simulation():
    #paramters for Monte Carlo simulation
    S_0 = 1.20  #Spot price
    r = 0.02  #Risk-free intrest rate 
    sigma = 0.25  #Volatility 
    T = 0.5  #Time to maturity (in years)
    num_simulations = 10000  #Number of simulations
    num_steps = 252  #Number of simulation steps (Note: We could use 252 * T = 126 trading days)

    # Time increment
    dt = T / num_steps

    # Simulating price paths
    rng = np.random.default_rng(42)  # For reproducibility
    price_paths = np.zeros((num_steps+1, num_simulations))
    price_paths[0] = S_0

    #changing the loop to start from 1 to num_steps+1 as to include maturity in the simulation
    for t in range(1, num_steps+1):

        #We let z be a stnd normal RV using numpy's standard normal function to generate random numbers for the simulation
        z = rng.standard_normal(num_simulations)
        #We price each path using geometric brownian motion 
        price_paths[t] = price_paths[t-1] * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * z)

    #Calculating the average simulated price at maturity
    average_simulated_price = np.mean(price_paths[-1])
    print(f"Average monte carlo simulated price at maturity: {average_simulated_price:.4f}")


# Set up a function to price European options using Monte Carlo simulation
def monte_carlo_option_price(
    S,
    K,
    T,
    r,
    sigma,
    option_type="call",
    num_simulations=100_000,
    seed=None,
):
    """Price a European option using Monte Carlo simulation."""
    #Validating the option type
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")

    #setting up a random number generator to generate standard normal random variables for the simulation
    rng = np.random.default_rng(seed)
    random_values = rng.standard_normal(num_simulations)

    #calculating the terminal stock prices at expiration using the geometric Brownian motion formula
    terminal_prices = S * np.exp(
        (r - 0.5 * sigma**2) * T
        + sigma * np.sqrt(T) * random_values
    )

    #Setting up the correct pay off functions based on the option type
    if option_type == "call":
        payoffs = np.maximum(terminal_prices - K, 0)
    else:
        payoffs = np.maximum(K - terminal_prices, 0)

    discounted_payoffs = np.exp(-r * T) * payoffs

    return float(np.mean(discounted_payoffs))


if __name__ == "__main__":
    monte_carlo_simulation()