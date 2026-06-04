from Quant_Project.black_scholes import put_option_price, call_option_price

#Example variables
S = 100  # Current stock price
K = 100  # Strike price
T=1    # Time to maturity (in years)
r = 0.05  # Risk-free interest rate 
sigma = 0.2  # Volatility of the stock
# Calculate call option price
call_price = call_option_price(S, K, r, sigma, T)
print(f"The price of the European call option is: {call_price:.2f}")

# Calculate put option price
put_price = put_option_price(S, K, r, sigma, T)
print(f"The price of the European put option is: {put_price:.2f}")