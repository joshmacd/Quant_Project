import numpy as np
import pytest

#Import the following functions from the binomial tree module and the black_scholes module
from quant_project.binomial_tree import (binomial_tree_call, binomial_tree_put, tree_parameters)
from quant_project.black_scholes import (call_option_price, put_option_price)


#We first reject any number of step 'N' that invalidate the tree. i.e n = 1,2,3,...
@pytest.mark.parametrize("N", [0, -1, 2.5, True, False, np.nan, np.inf])
def test_invalid_step_count(N):
    with pytest.raises(ValueError, match="N"):
        tree_parameters(T=1, r=0.05, sigma=0.2, N=N)


#Test every invalid value for each positive input and both option types.
@pytest.mark.parametrize("price_function", [binomial_tree_call, binomial_tree_put])

@pytest.mark.parametrize("parameter", ["S", "K", "T", "sigma"])

@pytest.mark.parametrize("value", [0, -1, np.nan, np.inf, -np.inf])


def test_invalid_positive_inputs(price_function, parameter, value):
    inputs = dict(S=100, K=100, T=1, r=0.05, sigma=0.2, N=100) #Create a dictonary of valid inputs as a benchmark
    inputs[parameter] = value #update the dictonary based on the inputs

    #Check that a value error related to the invalid parameter is raised
    with pytest.raises(ValueError, match=parameter):
        price_function(**inputs) #unpacking the dictonary into arguments


# Negative interest rates are allowed in this stock-price model. The resulting risk-neutral probability must still be valid.
@pytest.mark.parametrize("rate", [np.nan, np.inf, -np.inf]) #We reject NaN and infinite rates.
def test_nonfinite_interest_rate(rate):
    with pytest.raises(ValueError, match="r"):
        tree_parameters(T=1, r=rate, sigma=0.2, N=100)


#We now deal with invalid risk-neutral probability, that is, outside of the interval [0,1].
def test_invalid_risk_neutral_probability():
    with pytest.raises(ValueError, match="probability"):
        tree_parameters(T=1, r=1.0, sigma=0.01, N=1)


#We now ensure that the put-call parity is also satisfied.
@pytest.mark.parametrize("r", [-0.01, 0.0, 0.05])
def test_put_call_parity(r):
    S, K, T, sigma, N = 100, 110, 0.5, 0.25, 200
    
    #Define the put and call for some inputs
    call = binomial_tree_call(S, K, T, r, sigma, N)
    put = binomial_tree_put(S, K, T, r, sigma, N)

    # Allow an absolute difference of 1e-10 or a relative difference of 1e-10 times the expected value's magnitude, whichever is larger.
    assert call - put == pytest.approx(S - K * np.exp(-r * T), rel=1e-10, abs=1e-10)


#Compare fewer steps (coarse) with more steps (fine).It is important to note that increasing N reduces the time step dt = T / N.
@pytest.mark.parametrize(
    "tree_price, bs_price",[(binomial_tree_call, call_option_price), (binomial_tree_put, put_option_price),])

#We want to show that the fine binomial tree will produce a more accurate price than the coarse one
def test_convergence_to_black_scholes(tree_price, bs_price):
    inputs = dict(S=100, K=100, T=1, r=0.05, sigma=0.2) #set up a dictonary of entries and pass them to the bs_price function
    reference = bs_price(**inputs)

    #We now calculate the error in each tree
    coarse_error = abs(tree_price(**inputs, N=50) - reference) #We use 50 steps for the coarse tree
    fine_error = abs(tree_price(**inputs, N=1000) - reference) #We use 1000 steps for the fine tree

    # We assert that the error related to the fine tree is smaller than the coarse one
    assert fine_error < coarse_error
    assert fine_error < 0.005 # We check how close the fine tree price is to the black scholes price, smaller than 0.005 price units.