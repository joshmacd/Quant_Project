

## Overview

## Overview

This repository is being developed as a personal quantitative finance project. The aim is to implement core models and numerical methods used in derivatives pricing and risk analysis using clean Python code, testing and clear mathematical explanations.

Alongside the Python implementations, additional mathematical notes are being written in LaTeX to explore the theory underlying each model.

## Planned Features

- Black-Scholes pricing for European call and put options
- Binomial tree pricing for European and American options
- Monte Carlo pricing under geometric Brownian motion
- Greeks calculation
- Implied volatility estimation
- Convergence analysis and visualisation
- Value-at-Risk and Expected Shortfall extensions
- More to be added later
-

## Project Structure
text '''
Quant_Project/
├── .gitignore
├── LICENSE
├── README.md
├── pytest.ini
│
├── src/
│   └── quant_project/
│       ├── __init__.py
│       ├── black_scholes.py
│       ├── binomial_tree.py
│       ├── greeks.py
│       ├── implied_volatility.py
│       ├── monte_carlo.py
│       └── monte_carlo_option_pricing.py
│
├── tests/
│   ├── conftest.py
│   ├── convergance_binomial_tree.py
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   └── test_put_call_parity.py
│
├── examples/
│   ├── binomial_tree_example_call.py
│   ├── binomial_tree_example_put.py
│   ├── calculate_greeks.py
│   ├── implied_volatility_example.py
│   └── price_european_option.py
│
├── figures/
│   ├── binomial_convergence.py
│   └── binomial_convergence.pdf
│
└── notebooks/
    ├── Black_Scholes_Market.pdf
    ├── Github_notes
    └── Tex/
        └── Black_Scholes_market(Latex)
'''
## Technologies

- Python
- NumPy
- SciPy
- Matplotlib
- LaTeX
- Git / GitHub