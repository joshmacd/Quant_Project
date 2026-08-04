# This code is used to test the put-call parity relationship between call and put options.
# For details on the put-call parity relationship, please refer to the notes for the black scholes market.
#adding the necessary libraries for this testing module
import numpy as np
import pytest

#Importing the functions from the black scholes module
from quant_project.black_scholes import call_option_price, put_option_price

#We use pytest to test the put-call parity for a selection of inputs
@pytest.mark.parametrize(
    "S, K, T, r, sigma",
    [
        (100, 100, 1, 0.05, 0.2),
        (120, 100, 0.5, 0.03, 0.15),
        (80, 90, 2, 0.04, 0.25),
    ],
)
def test_put_call_parity(S, K, T, r, sigma):

    #This finds the price of a call option.
    call_price = call_option_price(S,K, T, r, sigma)

    #This finds the price of a put option.
    put_price = put_option_price(S, K, T, r, sigma)

    #We calculate both the left and right hand sides of the 
    #put-call parity equation.
    lhs = call_price - put_price
    rhs = S - K * np.exp(-r * T)

    #This asserts that the left and right sides are approximately equal.
    assert np.isclose(lhs, rhs), f"Put-call parity does not hold: {lhs} != {rhs}"