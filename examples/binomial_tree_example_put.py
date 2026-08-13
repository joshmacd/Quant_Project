from quant_project.binomial_tree import binomial_tree_put

#We will use the following paramaters to calculate the price of an EU put option
S=100 #Current stock price
K=100 #Strike price
T=1 #Time to maturity (in years)
r=0.05 #Risk-free interest rate
sigma=0.2 #Volatility of the stock
N=1 #Number of time steps in the binomial tree

#Then call on the function to calculate the price of the option
put_price = binomial_tree_put(S, K, T, r, sigma, N)
print(f"The price of the European put option is: {put_price:.4f}")
