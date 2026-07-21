#Improrting necessary libraries
import numpy as np
import scipy.stats as stats

#This function check whether the input are valid for the black scholes model.
#If the inputs are invalid, it will raise a value error.
def _validate_inputs(S, K, T, r, sigma):
    if S <= 0:
        raise ValueError("S must be greater than 0")
    if K <= 0:
        raise ValueError("K must be greater than 0")
    if T <= 0:
        raise ValueError("T must be greater than 0")
    if sigma <= 0:
        raise ValueError("sigma must be greater than 0")


def d1(S, K, T, r, sigma):
    '''
    Calculate the d1 parameter for the Black-Scholes model.
    inputs:
    ------
    S: Current stock price
    K: Strike price 
    r: Risk-free interest rate
    sigma: Volatility of the stock
    T: Time to maturity (in years)

    '''
    _validate_inputs(S, K, T, r, sigma)
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    '''
    Calculate the d2 parameter for the Black-Scholes model.
    inputs:
    ------
    S: Current stock price
    K: Strike price 
    r: Risk-free interest rate
    sigma: Volatility of the stock
    T: Time to maturity (in years)
    '''
    _validate_inputs(S, K, T, r, sigma)
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def call_option_price(S, K, T, r, sigma):
    '''
    Calculate the price of a European call option using the Black-Scholes model.
    inputs:
    ------
    S: Current stock price
    K: Strike price 
    r: Risk-free interest rate
    sigma: Volatility of the stock
    T: Time to maturity (in years)

    returns:
    -------
    call_price: The price of the European call option
    '''
    _validate_inputs(S, K, T, r, sigma)
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    
    call_price = S * stats.norm.cdf(D1) - K * np.exp(-r * T) * stats.norm.cdf(D2)
    
    return call_price

def put_option_price(S, K, T, r, sigma):
    '''
    Calculate the price of a European put option using the Black-Scholes model.
    inputs:
    ------
    S: Current stock price
    K: Strike price 
    r: Risk-free interest rate
    sigma: Volatility of the stock
    T: Time to maturity (in years)
    returns:
    -------
    put_price: The price of the European put option
    '''
    _validate_inputs(S, K, T, r, sigma)
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    
    put_price = K * np.exp(-r * T) * stats.norm.cdf(-D2) - S * stats.norm.cdf(-D1)
    
    return put_price