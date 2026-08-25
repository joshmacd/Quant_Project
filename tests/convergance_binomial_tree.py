#Here we test for convergence of the binomial tree model to the 
#Black-Scholes model for European call options. We will compare the option prices 
#obtained from both models for different numbers of time steps in the binomial tree.

import numpy as np
from quant_project.binomial_tree import binomial_tree_call 
from quant_project.black_scholes import call_option_price 

def convergence_test():
    #option parameters
    S0 = 100  # initial stock price
    K = 100   # strike price
    T = 1     # time to maturity in years
    r = 0.05  # risk-free interest rate
    sigma = 0.2  # volatility

    #We now calculate the price of an EU option using both models over a range of time steps
    time_steps = [1, 5, 10, 50, 100, 500, 1000]
    bs_price = call_option_price(S0, K, T, r, sigma)

    for i in time_steps:
        bt_price = binomial_tree_call(S0, K, T, r, sigma, i)
        print(f"Time Steps: {i}, Binomial Tree Price: {bt_price:.4f}, Black-Scholes Price: {bs_price:.4f}, Difference: {abs(bt_price - bs_price):.4f}") 

#running this files will execute the convergence test only when
# i excute this file directly.

if __name__ == "__main__":
    convergence_test()
