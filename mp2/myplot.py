# Based on code from: https://www.geeksforgeeks.org/python/how-to-plot-normal-distribution-over-histogram-in-python/

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def plot_normal_fit(data):

    # Fit a normal distribution to
    # the data:
    # mean and standard deviation
    mu, std = norm.fit(data) 

    # Plot the histogram.
    plt.hist(data, bins=25, density=True, alpha=0.6, color='b')

    # Plot the PDF.
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mu, std)

    plt.plot(x, p, 'k', linewidth=2)
    title = "Fit Values: {:.2f} and {:.2f}".format(mu, std)
    plt.title(title)

    plt.show()
    
    
    
def 