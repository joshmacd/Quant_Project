

## Overview

This repository is being developed as a personal quantitative finance project. The aim is to implement core models and numerical methods used in derivatives pricing and risk analysis using clean Python code, testing and clear mathematical explanations.

Alongside the Python implementations, additional mathematical notes are being written in LaTeX to explore the theory underlying each model.

## Implemented Features

- Black–Scholes pricing for European calls and puts.
- Analytical Greeks: delta, gamma, vega, theta, and rho.
- Cox–Ross–Rubinstein binomial pricing for European calls and puts.
- Monte Carlo pricing for European options under geometric Brownian motion.
- Implied volatility estimation using bisection.
- Binomial convergence examples and figures.

These implementations are under development. Automated testing currently focuses on Black–Scholes pricing, input validation, put–call parity, and analytical Greeks.

## Planned Features

- Broader automated tests for binomial pricing, Monte Carlo, and implied volatility.
- American-option pricing.
- Monte Carlo standard errors and confidence intervals.
- Newton–Raphson implied volatility with a robust fallback.
- Value at Risk and Expected Shortfall.
- Further convergence analysis and mathematical notes.

## Installation

Requires Python 3.11 or newer. From the repository root in Codespaces or macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev,plots]"
```

This installs the project in editable mode, including testing and plotting dependencies.

## Running Examples

With the virtual environment activated:

```bash
python examples/price_european_option.py
python examples/calculate_greeks.py
python examples/implied_volatility_example.py
```

## Running Tests

```bash
python -m pytest -v
```

The GitHub Actions workflow runs tests and the examples above on Python 3.11, 3.12, and 3.13 for pushes and pull requests. Check the Actions tab for the latest results.



## Project Structure

```text
Quant_Project/
├── src/quant_project/
│   ├── __init__.py
│   ├── black_scholes.py
│   ├── greeks.py
│   ├── binomial_tree.py
│   ├── monte_carlo.py
│   └── implied_volatility.py
├── examples/
│   ├── price_european_option.py
│   └── calculate_greeks.py
├── tests/
│   ├── conftest.py
│   ├── test_black_scholes.py
│   ├── test_greeks.py
│   ├── test_binomial_tree.py
│   └── test_put_call_parity.py
├── notebooks/
│   └── Black_Scholes_Market.pdf
├── figures/
├── pytest.ini
├── LICENSE
└── README.md
```
## Technologies

- Python
- NumPy
- SciPy
- Matplotlib
- LaTeX
- Git / GitHub
