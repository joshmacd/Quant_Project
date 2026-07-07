import numpy as np
from scipy.stats import norm
#This programme calculates the greeks of an option using the Black-Scholes model. 
#It includes functions to calculate delta, gamma, vega, theta, and rho for both call and put options.
#The main function, option_greeks, takes in the necessary parameters and returns a dictionary containing 
#the option price and its greeks based on the specified option type (call or put).

# Importing the necessary functions from the black_scholes module
from quant_project.black_scholes import (
    d1,
    d2,
    call_option_price,
    put_option_price,
)

#Defiining a function to caculate delta for call options
def call_delta(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return norm.cdf(d_1)

#Defining a function to calculate delta for put options
def put_delta(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return norm.cdf(d_1) - 1

#Defining a function to calculate gamma
def gamma(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return norm.pdf(d_1) / (S * sigma * np.sqrt(T))

#Defining a function to calc vega 
def vega(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    return S * norm.pdf(d_1) * np.sqrt(T)

#Defining a function to calc theta for a call option
def call_theta(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    d_2 = d2(S, K, T, r, sigma)

    return (
        -S * norm.pdf(d_1) * sigma / (2 * np.sqrt(T))
        - r * K * np.exp(-r * T) * norm.cdf(d_2)
    )

#Defining a function to calc theta for a put option
def put_theta(S, K, T, r, sigma):
    d_1 = d1(S, K, T, r, sigma)
    d_2 = d2(S, K, T, r, sigma)

    return (
        -S * norm.pdf(d_1) * sigma / (2 * np.sqrt(T))
        + r * K * np.exp(-r * T) * norm.cdf(-d_2)
    )

#Defining a function to calc rho for a call option
def call_rho(S, K, T, r, sigma):
    d_2 = d2(S, K, T, r, sigma)
    return K * T * np.exp(-r * T) * norm.cdf(d_2)

#Defining a function to calc rho for a put option
def put_rho(S, K, T, r, sigma):
    d_2 = d2(S, K, T, r, sigma)
    return -K * T * np.exp(-r * T) * norm.cdf(-d_2)

#Adding a control structure to ensure that the option_type parameter is either call or put.
def option_greeks(S, K, T, r, sigma, option_type="call"):
    option_type = option_type.lower()

    if option_type not in {"call", "put"}:
        raise ValueError("option_type must be either 'call' or 'put'.")
    #GGiven the the option type is a call option, the function returns the corresponding greeks
    if option_type == "call":
        return {
            "price": call_option_price(S, K, T, r, sigma),
            "delta": call_delta(S, K, T, r, sigma),
            "gamma": gamma(S, K, T, r, sigma),
            "vega": vega(S, K, T, r, sigma),
            "theta": call_theta(S, K, T, r, sigma),
            "rho": call_rho(S, K, T, r, sigma),
        }
    #Given the the option type is a put option, the function returns the corresponding greeks
    return {
        "price": put_option_price(S, K, T, r, sigma),
        "delta": put_delta(S, K, T, r, sigma),
        "gamma": gamma(S, K, T, r, sigma),
        "vega": vega(S, K, T, r, sigma),
        "theta": put_theta(S, K, T, r, sigma),
        "rho": put_rho(S, K, T, r, sigma),
    }