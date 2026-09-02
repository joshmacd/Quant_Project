#Importing the rquired modules from black scholes and implied volatility 
from quant_project.black_scholes import call_option_price
from quant_project.implied_volatility import implied_volatility_via_bisection

#Setting up the parameters for the option 
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.20

#Calculating the market price of the option using the Black-Scholes formula given
market_price = call_option_price(S, K, T, r, sigma)
print("market_price:", market_price)

imp_vol, iterations = implied_volatility_via_bisection(market_price, S, K, T, r, option_type="call", lower_bound=1e-6, upper_bound=5.0, tol=1e-6, max_iterations=300)

print("Implied volatility:", imp_vol)
print("Iterations:", iterations)

#The expected output of the code is:
#market_price: 10.450583572185565
#Implied volatility: 0.2000000242072642
#Iterations: 25