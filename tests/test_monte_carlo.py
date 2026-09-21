import numpy as np
import pytest

#Import relevent functions from the monte_carlo and black_scholes projects
from quant_project.monte_carlo import monte_carlo_option_price
from quant_project.black_scholes import (call_option_price, put_option_price)

#Define the option type testing enviroment, we want to check that having the return stat true doesnt affect the price
@pytest.mark.parametrize("option_type", ["call", "put"])
def test_stats_preserve_price(option_type):
    """Requesting statistics must not change the estimated price."""
    #Create a dictonary of inputs 
    inputs = dict( S=100, K=100, T=1, r=0.05, sigma=0.2, option_type=option_type, num_simulations=10000, seed=42)

    #Unpack the dictonary arguments and pass them as arguments
    price = monte_carlo_option_price(**inputs)
    result = monte_carlo_option_price(**inputs, return_stats=True) #Call again with return stats true

    #Check the price  is a float 
    assert isinstance(price, float)
    assert result["price"] == price
    assert result["standard_error"] > 0 #Check that standard error is positive 

    #Define the two end points of the condfidence interval as upper and lower
    lower, upper = result["confidence_interval"]
    margin = 1.96 * result["standard_error"] #The calculates the distance from each endpoint the the estimated price

    #We check that the confidence interval is constructed properly, where the pytest approx allows a small floating point tolerance
    assert lower == pytest.approx(price - margin)
    assert upper == pytest.approx(price + margin)

#We use the monkey patch tool from the pytest library
def test_statistics_from_known_payoffs(monkeypatch):
    """Check the calculations against two controlled random draws."""

    #We define an object to generate random numbers, which allows provide a method called standard normals
    class FixedGenerator:

        def standard_normal(self, size):
            '''
            self : The particular object recieving the request
            size : The number of draws requested
            '''
            #We want the size to be two as the will pricing function requests two draws
            assert size == 2
            return np.array([-1.0, 1.0]) #The method then returns a numpy array containing two values

    # Replace random sampling from np.random.defult_rng with Fixed generator for this test only.
    #The lambda defines a short function which takes the seed
    monkeypatch.setattr(np.random, "default_rng", lambda seed: FixedGenerator())

    result = monte_carlo_option_price(S=100, K=100, T=1, r=0.05, sigma=0.2, num_simulations=2,
        return_stats=True)

    #For these inputs, the GBM exponent is 0.03 + 0.2*Z, the first call payoff is zero; the second is positive.
    positive_payoff = np.exp(-0.05) * (100 * np.exp(0.23) - 100)

    # For observations [0, x], both the mean and the estimated standard error (using sample variance) are x/2.
    assert result["price"] == pytest.approx(positive_payoff / 2)
    assert result["standard_error"] == pytest.approx(positive_payoff / 2)

# Run a separate test for each invalid parameter/value pair, all other financial inputs remain valid in each test.
@pytest.mark.parametrize(
    "parameter, value",
    [
        ("S", 0),          
        ("K", -1),         
        ("T", 0),          
        ("sigma", -0.2),
        ("r", np.nan),    # The interest rate must be a finite number.
        ("S", np.inf),    # An infinite stock price is invalid.
        ("sigma", True),  # Reject booleans even though bool is a subclass of int.
        ("K", "100"),     # A numeric-looking string is still not a number.
    ],
)

def test_invalid_financial_inputs(parameter, value):
    #Define a dictonary containing a valid set of inputs
    inputs = dict(S=100, K=100, T=1, r=0.05, sigma=0.2)
    inputs[parameter] = value #Let one input equal one of its invalid inputs

    #Check that the correct error message is raised
    with pytest.raises(ValueError, match=parameter):
        monte_carlo_option_price(**inputs)

#We now test the count with invalid inpits, imporantly we can have anything strictly less than two
@pytest.mark.parametrize("count", [0, 1, -1, 2.5, True, np.nan, np.inf])
def test_invalid_simulation_count(count):
    #The error raised should identify the incorrect input
    with pytest.raises(ValueError, match="num_simulations"):
        #Fix all inputs and vary the number of simulations
        monte_carlo_option_price(S=100, K=100, T=1, r=0.05, sigma=0.2, num_simulations=count)

#check an unsupported string, an empty string, None, and an integer.
@pytest.mark.parametrize("option_type", ["invalid", "", None, 123])
def test_invalid_option_type(option_type):
    #expect an error that identifies the option_type argument
    with pytest.raises(ValueError, match="option_type"):
        #Similarly we vary only the option_types
        monte_carlo_option_price(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type=option_type,)


#pair each option type with its matching Black–Scholes function, function names have no parentheses because we pass the functions themselves - the test will call them later.
@pytest.mark.parametrize(
    "option_type, reference_function",
    [
        ("call", call_option_price),
        ("put", put_option_price),
    ],
)

#Combine both of the option types with both intrest rates
@pytest.mark.parametrize("r", [-0.01, 0.05]) #This should give us 4 test cases
def test_agreement_with_black_scholes(option_type, reference_function, r):
    #We create a dictonary to store a set of valid inputs
    inputs = dict(S=100, K=100, T=1, r=r, sigma=0.2)

    result = monte_carlo_option_price(**inputs, option_type=option_type, num_simulations=100_000,
        seed=42, return_stats=True) #The fixed seed make sure this is reproducable in the same enviroment

    #We then calculate the price of the option using the inputs that are passed to the function
    reference = reference_function(**inputs)

    #We then use tolerance for this regression check, correct simulation need not contain the reference price inside its 95% confidence interval on every run.
    error = abs(result["price"] - reference)

    #we allow a difference of up to five estimated standard errors, 
    assert error < 5 * result["standard_error"]
