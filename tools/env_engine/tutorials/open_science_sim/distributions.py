# %% [CELL 1: Imports]
import numpy as np
import matplotlib.pyplot as plt

# %% [CELL 2: Creating a random generator object]
rng = np.random.default_rng ()
# %% [CELL 3: Type of random number generator]
type (rng)

# %% [CELL 4: Helper Function]
def distribution_plot (samples, bins = 100, figsize = (5, 3)):
    '''
    # Helper Function to visualise the distributions

    Params:
    ------
    samples: np.ndarray
        A numpy array

    bins: int, optional (default = 100)
        The number of bins to include in the histogram

    figsize: (int, int) (default = (5, 3))
        Size of the plot in pixels

    Returns:
    -------
        fig, ax: a tuple containing matplotlib figure and axis objects
    '''

    hist = np.histogram (samples, bins = np.arange (bins),
                         density = True)
    
    fig = plt.figure (figsize = figsize)
    ax = fig.add_subplot ()
    _ = ax.plot (hist[0])
    _ = ax.set_ylabel ('p (x)')
    _ = ax.set_xlabel ('x')

    return fig, ax


