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
def monte_carlo_option_price(S, K, T, r, sigma, option_type="call", num_simulations=100_000, seed=None, return_stats = False):
    """ Estimate a European option price using Monte Carlo simulation.
    
    In this function we sample terminal stock prices under risk-neutral geometric brownian
    motion. The function calculate the option payoffs, and return their discounted
    sample mean. Assumes constant interest rate and volatility on a non-divedend paying stock.

    Parameters
    ----------
    S : Current stock price. Must be finite and strictly positive.
    K : Strike price. Must be finite and strictly positive.
    T : Time to maturity in years. Must be finite and strictly positive.
    r: Annualised risk-free interest rate, must be finite; negative rates are permitted.
    sigma: Annualised volatility, must be finite and strictly positive.
    option_type : Either "call" or "put".
    num_simulations : Number of independent terminal stock prices to simulate.
    seed : Seed for NumPy's random number generator. A fixed seed makes results reproducible.
    return_stats : If True returns the price and uncertanity statistics, standard error, a 95% confidence interval.

    Returns
    -------
    Estimated option price in the same currency units as S and K, and as a float

    Raises
    ------
    ValueError
        If a financial input is non-numeric or non-finite, if S, K, T, or sigma is non-positive, if option_type is invalid, or
        if num_simulations is not an integer of at least 2. Boolean financial inputs and simulation counts are rejected.

    """


    # Start by checking the numerical inputs - interest rates may be negative; the other inputs must be positive.
    inputs = {"S": S, "K": K, "T": T, "r": r, "sigma": sigma}

    for name, value in inputs.items():
        # Reject booleans, strings, and other non-numeric inputs.
        if isinstance(value, (bool, np.bool_)) or not isinstance(
            value, (int, float, np.integer, np.floating)
        ):
            raise ValueError(f"{name} must be a finite real number")

        # NaN and infinity must not enter the pricing calculation.
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")

        if name != "r" and value <= 0:
            raise ValueError(f"{name} must be greater than 0")

    # Require a whole number of simulations.
    # We require at least two because the upcoming standard-error
    # calculation needs a sample variance, which uses n - 1.
    if (
        isinstance(num_simulations, (bool, np.bool_))
        or not isinstance(num_simulations, (int, np.integer))
        or num_simulations < 2
    ):
        raise ValueError("num_simulations must be an integer of at least 2")

    #Check that option type is a string
    if not isinstance(option_type, str):
        raise ValueError("option_type must be 'call' or 'put'")

    option_type = option_type.lower() #This allows call or put to contain capitals, like Put or CALL

    #Check that we have either a call or put
    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be 'call' or 'put'")


    #setting up a random number generator to generate standard normal random variables for the simulation
    rng = np.random.default_rng(seed)
    random_values = rng.standard_normal(num_simulations)

    #calculating the terminal stock prices at expiration using the geometric Brownian motion formula
    terminal_prices = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * random_values)

    #Setting up the correct pay off functions based on the option type
    if option_type == "call":
        payoffs = np.maximum(terminal_prices - K, 0)
    else:
        payoffs = np.maximum(K - terminal_prices, 0)

    #We discount the maturity payoffs back to today.
    discounted_payoffs = np.exp(-r * T) * payoffs

    #Calculate the option price using the average discounted payoff
    price = float(np.mean(discounted_payoffs))

    #measure the variation between individual discounted payoffs.
    payoff_std = float(np.std(discounted_payoffs, ddof=1))

    #Calculate the sampling uncertainty in the average price.
    standard_error = float(payoff_std / np.sqrt(num_simulations))

    #The construct a 95% confidence interval
    confidence_interval = ( price - 1.96 * standard_error, price + 1.96 * standard_error)

    #We return the price and uncertainty statistics, if return stats is true.
    if return_stats:
        return {"price": price, "standard_error": standard_error, "confidence_interval": confidence_interval}

    return price


if __name__ == "__main__":
    monte_carlo_simulation()