#This file is used to test the function in the black_scholes.py file.
#A few tests are used to ensure that the function is working correctly and returning the expected results. 
#These consist  check the outputs with known values, using the put-call parity relationship.
#We should also test the function with different input values to ensure that it is robust - this will have to be implemented into the code first.

import pytest

from quant_project.black_scholes import call_option_price, put_option_price


def test_black_scholes_call():
    #Here we compare the outputs of the call  option prices with known values - 
    # please refer to the notes for the black scholes market.
    S = 100 #Stock price
    K = 100 #Strike
    T = 1 #Time until maturity
    r = 0.05 #Risk free rate
    sigma = 0.2 #Volatility
    call_price = call_option_price(S, K, T, r, sigma)
    assert round(call_price, 6) == 10.450584

def test_black_scholes_put():
    #Here we compare the outputs of the put option prices with known values - 
    # please refer to the notes for the black scholes market.
    S = 100 #Stock price
    K = 100 #Strike
    T = 1 #Time until maturity
    r = 0.05 #Risk free rate
    sigma = 0.2 #Volatility
    put_price = put_option_price(S, K, T, r, sigma)
    assert round(put_price, 6) == 5.573526

#Here we are testing to ensure we are getting value error for incorrect inputs
def test_invalid_inputs_raise_value_error():
    with pytest.raises(ValueError):
        call_option_price(0, 100, 1, 0.05, 0.2)

    with pytest.raises(ValueError):
        put_option_price(100, 0, 1, 0.05, 0.2)

    with pytest.raises(ValueError):
        call_option_price(100, 100, 0, 0.05, 0.2)

    with pytest.raises(ValueError):
        call_option_price(100, 100, 1, 0.05, 0)

    with pytest.raises(ValueError):
        call_option_price(100, 100, 1, 0.05, -0.2)


    #Run pytest in the terminal to run the test and check that the function is working correctly.
    # PYTHONPATH=src pytest -v