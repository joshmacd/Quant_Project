#Importing the necessary libraries
import numpy as np


def _validate_number(name, value, *, positive=False):
    """Require a finite real number, optionally strictly positive.
    --------------------------------------------------------------
    name is used in error messages, such as "S must be finite".
    positive=True additionally requires the value to exceed zero.
    
    """
    #python treats booleans as integers (i.e: True = 1), the isinstance function checks if the value is a specfic data type and return either T or F
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, (int, float, np.integer, np.floating)):
        raise ValueError(f"{name} must be a finite real number")

    #Raise an error if the value is NaN or infinity
    if not np.isfinite(value):
        raise ValueError(f"{name} must be finite")

    
    if positive and value <= 0:
        raise ValueError(f"{name} must be greater than 0")


def tree_parameters(T, r, sigma, N):
    """
    Calculate the Cox–Ross–Rubinstein tree parameters.

    Inputs:
        T: Time to maturity in years.
        r: Continuously compounded risk-free interest rate.
        sigma: Annualised volatility.
        N: Positive integer number of time steps.

    Returns:
        dt: Time step size.
        u: Up factor.
        d: Down factor.
        p: Risk-neutral up probability.
        q: Risk-neutral down probability.
    """
    if (isinstance(N, (bool, np.bool_)) or not isinstance(N, (int, np.integer)) or N <= 0):
        raise ValueError("N must be a positive integer")

    #Validate the time to maturity, intrest rate and volatility
    _validate_number("T", T, positive=True)
    _validate_number("r", r)
    _validate_number("sigma", sigma, positive=True)

    dt = T / N #define the time step
    u = np.exp(sigma * np.sqrt(dt)) #define the 'up factor'
    d = 1 / u #define the 'down factor'

    p = (np.exp(r * dt) - d) / (u - d) #define the 'up probability'
    q = 1 - p #define the 'down probability'

    #Ensure the the probability is contained in the closed interval 
    if not 0 <= p <= 1:
        raise ValueError("Risk-neutral probability must be between 0 and 1")

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

    #Set up the price process and validate the strike and stock price
    _validate_number("S", S, positive=True)
    _validate_number("K", K, positive=True)

    dt, u, d, p, q = tree_parameters(T, r, sigma, N)

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


def binomial_tree_put(S, K, T, r, sigma, N):
    '''
    This function calculates the price of a EU put option using the
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
    put_price: The price of the European put option
    '''

    #Set up the price process and validate the 
    _validate_number("S", S, positive=True)
    _validate_number("K", K, positive=True)

    dt, u, d, p, q = tree_parameters(T, r, sigma, N)

    #Initalise the up and down movements of the stock price
    j = np.arange(N+1) #This is the number of up movements in the stock price

    #Calculate the final stock price for each node.
    terminal_stock_price = S * (u**j) * (d**(N-j))

    #calculate the option value at each terminal node
    terminal_option_value = np.maximum(K - terminal_stock_price, 0) #For call option (S-K)^+ - put (K-S)^+

    #Find the discounting factor of the call option 
    Z = np.exp(-r * dt)

    #Then using backwards induction we calculate the option price at each node of the tree
    for i in range(N-1, -1, -1):
        terminal_option_value = Z * (p * terminal_option_value[1:i+2] + q * terminal_option_value[0:i+1])
    
    return terminal_option_value[0]