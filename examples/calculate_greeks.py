from quant_project.greeks import option_greeks

#We will calculate the greeks for a call option with the following parameters:
#possible issue could be that we take negative values for the parameters, which would not make sense in the context 
#of option pricing - hence we could improve via ristricting the input values to be correct
S = 100
K = 100
T = 1
r = 0.05
sigma = 0.2

#Calls on the option_greeks function
results = option_greeks(S, K, T, r, sigma, option_type="call")

#Printing reults 
print("Black-Scholes Greeks")
print("--------------------")

for name, value in results.items():
    print(f"{name}: {value:.6f}")

# PYTHONPATH=src python examples/calculate_greeks.py
# Expected output:
# Black-Scholes Greeks
#--------------------
#price: 18.126925
#delta: 1.000000
#gamma: 0.000000
#vega: 0.000000
#theta: -4.756147
#rho: 95.122942