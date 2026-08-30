#importing the necessary libraries
import numpy as np

#importing the necessary functions from the black_scholes module
from quant_project.black_scholes import (call_option_price, put_option_price)

def implied_volatility_via_bisection(
    marketprice,
    S,
    K,
    T, 
    r,
    option_type = "call",
    lower_bound = 1e-6,
    upper_bound = 5.0,
    tol = 1e-6,
    max_iterations = 300
):

''' Calculate the implied volatility of a European option using the bisection method. This function using newton-raphson method the narrow down
    the range of possible volatilities until it finds a value that produces a theorectical option price that is close 'enough' to the market price of an option using 
    the black - scholes fomula.

    inputs:
        marketprice: The market price of the option.
        S: The current stock price.
        K: The strike price of the option.
        T: The time to maturity.
        r: The risk-free interest rate.
        option_type: "call" for call options, "put" for put options.
        lower_bound: Lower bound for volatlity search (1e-6).
        upper_bound: Upper bound for volatility search ( 5.0).
        tol: Tolerance for convergence ( 1e-6).
        max_iterations: Maximum number of iterations ( 300).

    returns:
        The implied volatility of the option and the number of iterations it took to converge.
    '''

    #Validating the option parameters
    if S <= 0:
        raise ValueError("Stock price must be positive.")
    if K <= 0:
        raise ValueError("Strike price must be positive.")
    if T <= 0:
        raise ValueError("Time to maturity must be positive.")
    
    option_type = option_type.lower()
    if option_type not in ["call", "put"]:
        raise ValueError("option_type must be 'call' or 'put'")
    
    #Calculate the discounted strike price of the option
    discounted_strike = K * np.exp(-r * T)

    #Choose the correct option type and payoff function assicated with it
    if option_type == "call":
        option_price_func = call_option_price
        min_price = max(0.0, S - discounted_strike)
        max_price = S
    else:
        option_price_func = put_option_price
        min_price = max(0.0, discounted_strike - S)
        max_price = discounted_strike

    # Check the market price assumption which bound the market price between the min and max price of the option equivalently the non-abritrage bounds
    if marketprice < min_price or marketprice > max_price:
        raise ValueError("Market price is not within the valid range for the given option parameters.")

    #Initalise the lower and uppper price bounds for the biscetion method
    lower_price_bound = price_function(S,K,T,r, lower_volatility)
    upper_price_bound = price_function(S,K,T,r, upper_volatility)

    #next is the root-finding method - first check the volatility interval contains a soln then using loop over each itteration 
    #using the bisection method (a+b)/2 find a midpoint volatilty abd set it as the market volatility . Finally test for convergance

