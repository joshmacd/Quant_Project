#This code is used to test the put-call parity relationship between call and put options.
#For details on the put-call parity relationship, please refer to the notes for the black scholes market.

from quant_project.black_scholes import call_option_price


def test_put_call_parity(S, K, T, r, sigma):

    #This finds the price of acall option 
    call_price = call_option_price(S, K, T, r, sigma)

    #This finds the price of a put option
    put_price = put_option_price(S, K, T, r, sigma)

    #This is the left-hand side of the put call parity, the difference between the call and put prices
    lhs = call_price - put_price

    #This is the righ-hand side of the put call parity
    rhs = S - K * np.exp(-r * T)

    #This test that the left and right side are approximately equal up to some rounding error.
    #If they are not equal the assertion will fail - that is the put call parity does not hold.
    assert np.isclose(lhs, rhs), f"Put-call parity does not hold: {lhs} != {rhs}"

#Testing the put call parity test with the following parameters:
test_put_call_parity(100,100,1,0.05,0.2)
