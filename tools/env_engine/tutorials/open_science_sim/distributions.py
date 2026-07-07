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

# SAMPLING
# %% [CELL 5: Uniform Distribution]
# Step 1: create a random number generator, set seed to 42
rng = np.random.default_rng (45)

# Step 2 and 3: call the appropiate method of the generator and store result
samples = rng.uniform (low = 10, high = 40, size = 1_000_000)

# Ilustrate with plot
plot = distribution_plot (samples, bins = 50)

# %% [CELL 6: Exponential distribution]
rng = np.random.default_rng (45)
samples = rng.exponential (scale = 12, size = 1_000_000)
_ = distribution_plot (samples, bins = 50)

# %% [CELL 7: Normal distribution]
rng = np.random.default_rng (45)
samples = rng.normal (loc = 25.0, scale = 5.0, size = 1_000_000)
_ = distribution_plot (samples, bins = 50)

# Generating a single sample
# %% [CELL 8: Return type]
rng = np.random.default_rng (45)
sample = rng.normal (loc = 25.0, scale = 5.0)
print (sample)
print (type (sample))

# %% [CELL 9: Return an array]
rng = np.random.default_rng (45)
sample = rng.normal (loc = 25.0, scale = 5.0, size = 1)
# a numpy array is returned
print (sample)
print (type (sample))

# Accessing the scalar value using the 0 index of the array
print (sample[0])

# Spawning multiple non-overlapping PRN streams
# %% [CELL 10: Creating seeds from a single user supplied seed]
n_streams = 2
user_seed = 1

seed_sequence = np.random.SeedSequence (user_seed)
seeds = seed_sequence.spawn (n_streams)

# %% [CELL 11: Using seeds when creating our PRNGs. Ex: One for inter-arrival times & one for service times]
# e.g. to model arrival times
arrival_rng = np.random.default_rng (seeds[0])

# e.g. to model service times
service_rng = np.random.default_rng (seeds[1])

# Enscapulating distributions, params, and random seeds]
# %% [CELL 12: Instantiate two Exponential objects for two different purposes: acute length of stay, and rehab length of stay]
class Exponential:
    '''
    Convenience class for the exponential distribution
    Packages up distribution params, seed and random generator
    '''

    def __init__ (self, mean, random_seed = None):
        '''
        Constructor

        Params:
        ------
        mean: float
            The mean of the exponential distribution
        
        random_seed: int | SeedSequence, optional (default = None)
            A random seed to reproduce samples. If set to none then a unique
            sample is created
        '''
        self.rand = np.random.default_rng (seed = random_seed)
        self.mean = mean

    def sample (self, size = None):
        '''
        Generate a sample from the exponential distribution

        Params:
        -------
        size: int, optional (default = None)
            the number of samples to return. If size = None then a single
            sample is returned
        '''
        return self.rand.exponential (self.mean, size = size)
        
# %% [CELL 13: Creating the models]
acute_los = Exponential (3.0, random_seed = 45)
rehab_los = Exponential (30.0, random_seed = 105)

# %% [CELL 14: Distributing sample for acute_los]
acute_los.sample ()

# %% [CELL 15: Distributing sample for rehab_los]
rehab_los.sample ()

