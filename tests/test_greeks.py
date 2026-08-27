#This code is used to test each of the greeks against a numerical
# finite difference approximation. The exact details of this can be 
#found in the notes for the greeks(yet to be completed).

#importing the necessary libraries
import numpy as np
import pytest

#Importing functions from the greeks and black scholes modules
from quant_project.greeks import option_greeks
from quant_project.black_scholes import (call_option_price, put_option_price)

#Set up the pytest parameterisation
@pytest.mark.parametrize(
    "option_type, price_function",
    [
        ("call", call_option_price),
        ("put", put_option_price),
    ],
)

#This function tests the greeks against a numerical finite difference approximation.
def test_greeks(option_type, price_function):
    #Set up the parameters for the test
    S = 100  # Current stock price
    K = 100  # Strike price
    T = 1    # Time to expiration in years
    r = 0.05 # Risk-free interest rate
    sigma = 0.2 # Volatility

    #Calculate the option price and greeks 
    greeks = option_greeks(S, K, T, r, sigma, option_type)
    
    #Calculate the option price using the Black-Scholes formula
    option_price = price_function(S, K, T, r, sigma)

    #The finite fifference step sizes for time, spot price, volatility and intrest rate.
    spot_step = 0.01 
    volatility_step = 1e-5
    time_step = 1e-5
    rate_step = 1e-5

    #Finite difference approximation for delta
    delta_fd = (price_function(S + spot_step, K, T, r, sigma) - price_function(S - spot_step, K, T, r, sigma)) / (2 * spot_step)
    
    #Finite difference approximation for gamma
    gamma_fd = (price_function(S + spot_step, K, T, r, sigma) 
    - 2 * option_price + price_function(S - spot_step, K, T, r, sigma)) / (spot_step ** 2)
    
    #Finite difference approximation for vega
    vega_fd = (price_function(S, K, T, r, sigma + volatility_step)
     - price_function(S, K, T, r, sigma - volatility_step)) / (2 * volatility_step)
    
    #Finite difference approximation for theta
    theta_fd = -(price_function(S, K, T + time_step, r, sigma)
    - price_function(S, K, T - time_step, r, sigma)) / (2 * time_step)

    #Finite difference approximation for rho
    rho_fd = (price_function(S, K, T, r + rate_step, sigma) - 
    price_function(S, K, T, r - rate_step, sigma)) / (2 * rate_step)

    # Assert that the analytical and finite difference approximations are close

    tol = 1e-4 #The tolerance for the comparison
    
    assert np.isclose(greeks['delta'], delta_fd, rtol=tol, atol=tol), f"Delta mismatch: {greeks['delta']} vs {delta_fd}"
    assert np.isclose(greeks['gamma'], gamma_fd, rtol=tol, atol=tol), f"Gamma mismatch: {greeks['gamma']} vs {gamma_fd}"
    assert np.isclose(greeks['vega'], vega_fd, rtol=tol, atol=tol), f"Vega mismatch: {greeks['vega']} vs {vega_fd}"
    assert np.isclose(greeks['theta'], theta_fd, rtol=tol, atol=tol), f"Theta mismatch: {greeks['theta']} vs {theta_fd}"
    assert np.isclose(greeks['rho'], rho_fd, rtol=tol, atol=tol), f"Rho mismatch: {greeks['rho']} vs {rho_fd}"
