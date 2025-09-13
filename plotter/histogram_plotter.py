# Based on code from: https://www.geeksforgeeks.org/python/how-to-plot-normal-distribution-over-histogram-in-python/

import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Function for plotting a single histogram with normal curve fitted
def plot_histogram(data):

    # Fit a normal distribution to the data
    mean, std = norm.fit(data)

    # Plot the histogram
    plt.hist(data, bins=25, density=True, alpha=0.6, color='b')

    # Plot the Probability Density Function
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = norm.pdf(x, mean, std)

    plt.plot(x, p, 'k', linewidth=2)
    
    
    
# Function for plotting histograms with normal curve fitted for all numeric columns in a data frame
def plot_histograms_for_data_frame(df):

    # Number of plots to make (one plot for each column in the data frame)
    num_plots = len(df.columns)

    # Determine subplot grid size
    ncols = 3
    nrows = int(np.ceil(num_plots / ncols))

    # Create figure and axes
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5 * nrows))
    axes = axes.flatten()  # Flatten in case it's 2D

    # Loop through columns and plot
    for i, column in enumerate(df.columns):
        plt.sca(axes[i])  # Set current axis
        plot_histogram(df[column])
        axes[i].set_title(column)

    # # Hide any unused subplots
    # for j in range(i + 1, len(axes)):
    #     fig.delaxes(axes[j])

    plt.tight_layout()