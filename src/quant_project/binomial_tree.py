#Importing the necessary libraries
import numpy as np

def tree_parameters(T, r, sigma, N):
    '''
    This function calculates the parameters for the binomial tree model.
    Set up a testing module to check validity of the parameters.

    inputs:
    ------
    T: Time to maturity (in years)
    r: Risk-free interest rate
    sigma: Volatility of the stock
    N: Number of time steps in the binomial tree

    returns:
    -------
    u: Up factor
    d: Down factor
    p: Risk-neutral probability
    q : 1-p, the probability of a down movement
    dt: Time step size
    '''

    #Parameter validation
    if N <= 0:
        raise ValueError("N must be greater than 0") #The number of time steps must be a positive intger

    if sigma <= 0:
        raise ValueError("sigma must be greater than 0") #Volatility must be a positive integer

    if not 0 <= p <= 1:
        raise ValueError("Non-Arbitage Condition Failed:Risk-neutral probability must be between 0 and 1") 
        #Risk neutral probability must be between 0 and 1.

    #Calculate the time step 
    dt = T / N

    #Calculate the up and down factors
    u = np.exp(sigma *np.sqrt(dt))
    d = 1/u # Check the no arbitrage cond (d<e^rt<u which ensures 0<p<1).

    #Calculate the risk-neutral probability
    p = (np.exp(r *dt) - d) / (u-d) 
    q = 1-p # This is the probability of a down movement


    return dt, u, d, p, q

def binomial_tree_call(S, K, T, r, sigma, N):
    '''
    This function calculates the price of a EU call option using the
    Cox-Ross-Rubinstein Model or the binomial tree model.

    inputs:
    ------
    S: Current stock price
    K: Strike price
    T: Time to maturity (in years)
    r: Risk-free interest rate
    sigma: Volatility of the stock
    N: Number of time steps in the binomial tree
    
    returns:
    -------
    call_price: The price of the European call option
    '''

    #Set up the price process 
    dt, u, d, p, q = tree_parameters(T,r, sigma, N)

    #Initalise the up and down movements of the stock price
    j = np.arange(N+1) #This is the number of up movements in the stock price

    #Calculate the final stock price for each node.
    terminal_stock_price = S * (u**j) * (d**(N-j))

    #calculate the option value at each terminal node
    terminal_option_value = np.maximum(terminal_stock_price - K, 0) #For call option (S-K)^+ - put (K-S)^+

    #Find the discounting factor of the call option 
    Z = np.exp(-r * dt)

    #Then using backwards induction we calculate the option price at each node of the tree
    for i in range(N-1, -1, -1):

        terminal_option_value = Z * (p * terminal_option_value[1:i+2] + q * terminal_option_value[0:i+1])
    return terminal_option_value[0]
