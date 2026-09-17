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
        (100, 100, 1, 0.05, 0.20),
        (80, 100, 0.25, 0.03, 0.30),
        (120, 100, 2, 0.07, 0.15),
        (100, 110, 0.5, -0.01, 0.25),
    ],
)
def test_put_call_parity(S, K, T, r, sigma):

    #This finds the price of a call option.
    call_price = call_option_price(S,K, T, r, sigma)

    #This finds the price of a put option.
    put_price = put_option_price(S, K, T, r, sigma)

    #using numpy's isclose function where atol is the absolute tolerance parameter and rtol is the relative tolerance parameter
    assert np.isclose(
        call_price - put_price,
        S - K * np.exp(-r * T),
        rtol=1e-10,
        atol=1e-10,
    )

#Using pytest to parameterise the price functions and the inputs for our tests
@pytest.mark.parametrize(
    "price_function", [call_option_price, put_option_price]
)
@pytest.mark.parametrize(
    "inputs",
    [
        (0, 100, 1, 0.05, 0.2),
        (100, 0, 1, 0.05, 0.2),
        (100, 100, 0, 0.05, 0.2),
        (100, 100, 1, 0.05, 0),
        (100, 100, 1, 0.05, -0.2),
    ],
)

#Define a function to test some invalid inputs and test the program under these inputs
def test_invalid_inputs(price_function, inputs):
    with pytest.raises(ValueError):
        price_function(*inputs)

# cd /workspaces/Quant_Project PYTHONPATH=src pytest tests/test_put_call_parity.py