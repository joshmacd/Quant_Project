from quant_project.black_scholes import (
    call_option_price,
    put_option_price,
)
from quant_project.monte_carlo import monte_carlo_option_price

#This function calculates the option price using the Monte Carlo simulation and 
#compares it to the Black-Scholes price.

def test_monte_carlo_option_price():
    #The option parameters
    S = 100  # Current stock price
    K = 100  # Strike price
    T = 1    # Time to expiration in years
    r = 0.05 # Risk-free interest rate
    sigma = 0.2 # Volatility

    #Monte Carlo estimates for call option
    mc_call_price = monte_carlo_option_price(
        S = S,
        K = K,
        T = T,
        r = r,
        sigma = sigma,
        option_type = "call",
        num_simulations = 100000,
        seed = 42,
    )

    #monte carlo estimates for put option
    mc_put_price  = monte_carlo_option_price(
        S=S,
        K = K,
        T = T,
        r = r,
        sigma = sigma,
        option_type = "put",
        num_simulations = 100000,
        seed = 42,
    )

    #Calculate the Black-Scholes price for a comparison
    bs_call_price = call_option_price(S, K, T, r, sigma)
    bs_put_price = put_option_price(S, K, T, r, sigma)

    print("European option pricing comparison")
    print("----------------------------------")
    print(f"Monte Carlo call:  {mc_call_price:.4f}")
    print(f"Black-Scholes call: {bs_call_price:.4f}")
    print()
    print(f"Monte Carlo put:   {mc_put_price:.4f}")
    print(f"Black-Scholes put:  {bs_put_price:.4f}")
    print()
    print(f"Difference call:   {abs(mc_call_price - bs_call_price):.4f}")
    print(f"Difference put:    {abs(mc_put_price - bs_put_price):.4f}")

#This will allow to code to run.
if __name__ == "__main__":
    test_monte_carlo_option_price()