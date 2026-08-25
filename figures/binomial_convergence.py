from pathlib import Path
#Here we are using matplotlib to generate a figure to compare convergance
import matplotlib.pyplot as plt 

#Importing the black scholes and binomial tree models
from quant_project.binomial_tree import binomial_tree_call
from quant_project.black_scholes import call_option_price

#define a function to generate the convergance figures
def create_convergence_figure():
    S = 100
    K = 100
    T = 1
    r = 0.05
    sigma = 0.2

    #Defining an array of time steps to use for binom tree
    time_steps = [10, 20, 50, 100, 200, 500, 1000]
    bs_price = call_option_price(S, K, T, r, sigma)

    #initialise empty arrays to store the binomial tree prices and also errors
    tree_prices = []
    errors = []
    
    #looping over the time steps and calculating the binomial tree price at each time step
    for i in time_steps:
        tree_price = binomial_tree_call(
            S, K, T, r, sigma, i
        )
        #also calculate the error between the two prices
        eps = abs(tree_price - bs_price)

        tree_prices.append(tree_price)
        errors.append(eps)

        print(
            f"Steps: {i:4d}, "
            f"Tree price: {tree_price:.6f}, "
            f"Black-Scholes price: {bs_price:.6f}, "
            f"Error: {eps:.6f}"
        )

    #setting up the figure and axes
    figure, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(
        time_steps,
        tree_prices,
        marker="o",
        label="Binomial tree",
    )

    axes[0].axhline(
        bs_price,
        color="red",
        linestyle="--",
        label="Black-Scholes",
    )

    axes[0].set_xscale("log")
    axes[0].set_xlabel("Number of time steps")
    axes[0].set_ylabel("European call price")
    axes[0].set_title("Binomial Tree Convergence")
    axes[0].grid(alpha=0.3)
    axes[0].legend()

    axes[1].plot(
        time_steps,
        errors,
        marker="o",
        color="darkorange",
    )
    axes[1].set_xscale("log")
    axes[1].set_yscale("log")
    axes[1].set_xlabel("Number of time steps")
    axes[1].set_ylabel("Error in absolute pricing")
    axes[1].set_title("error in convergence Error")
    axes[1].grid(alpha=0.3)

    figure.tight_layout()

    #This will save beside this Python file, regardless of working directory.
    output_path = Path(__file__).with_name(
        "binomial_convergence.pdf"
    )
    figure.savefig(output_path, format="pdf", bbox_inches="tight")
    plt.close(figure)

    print(f"Figure saved to: {output_path}")


if __name__ == "__main__":
    create_convergence_figure()