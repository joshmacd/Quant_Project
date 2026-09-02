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


    ''' Calculate the implied volatility of a European option using the bisection method. This function using bisection method the narrow down
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

    #Initalise the lower and uppper price bounds for the biscetion method at the lower and upper bounds for volatility
    lower_price_bound = option_price_func(S, K, T, r, lower_bound)
    upper_price_bound = option_price_func(S, K, T, r, upper_bound)

    #Checking if the market price is between the lower and upper price bounds to see if we have a solution in the volatility interval
    if marketprice < lower_price_bound or marketprice > upper_price_bound:
        raise ValueError("Market price is not within the valid range for the given volatility bounds.")

    #Now use the bisection method to find the implied volatility
    for iteration in range(1, max_iterations + 1):

        #initalise the midpoint volatity and calculate the option price at that given volatility
        mid_vol = (lower_bound + upper_bound) / 2
        mid_price = option_price_func(S, K, T, r, mid_vol)

        #Now we check if how close the midpoint price is to the 'market price'
        if abs(mid_price - marketprice) < tol:
            return mid_vol, iteration

        #We adjust bounds based on the comparison of the midpoint price and the market price to shrink the inteval 
        if mid_price < marketprice:
            lower_bound = mid_vol
        else:
            upper_bound = mid_vol
    
    #raise an error if the bisection mehtod doesnt converge with the max number of iterations
    raise RuntimeError("Bisection method did not converge within the maximum number of iterations.")