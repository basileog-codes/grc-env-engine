# %% [CELL 1: Imports]
import simpy

# Building the model blocks

# %% [CELL 2.1: SimPy environment]
env = simpy.Environment ()

# %% [CELL 2.2: SimPy timeouts]
env.timeout (1.0)

# %% [CELL 2.3: Generators]
def arrivals_generator (env):
    while True:
        yield env.timeout (1.0)

# 2.4 SimPy process & run

# %% [1. Set the generator up as a SimPy process]
env.process (arrivals_generator (env))

# %% [2. Run the environment for a user specified length using env.run ()]
env.run (until = 25)

# %% [CELL 3: Creating the Model]
def arrivals_generator (env):
    '''
    Callers arrive with a fixed inter-arrival time of 1.0 minutes.

    Params:
    env: simpy.Environment
    '''

    # There won't be an infinite loop problem.
    # SimPy will exit at the correct time

    while True:

        # sample an inter-arrival time
        inter_arrival_time = 1.0

        # use the yield keyword instead of return
        yield env.timeout (inter_arrival_time)

        #  print out the time of the arrival
        print (f'call arrives at: {env.now}')

# %% [CELL 4: Creating RUN_LENGTH param that we can model for different time lengths]

# model params
RUN_LENGTH = 25

# create the simpy environment object
env = simpy.Environment ()

# tell simpy that the 'arrivals_generator' is a process
env.process (arrivals_generator (env))

# run the simulation model
env.run (until = RUN_LENGTH)
print (f'end of run. simulation clock time = {env.now}')

# ----------------------------------------------------------------------------------------
# Exercise: Modelling a poison arrival for prescriptions
# Task:
# Update arrivals_generator () so that the inter-arrival times follow an exponential
# distribution with a mean inter-arrival time of 60.0 minutes / 100 arrivals between arrivals
# (i.e. 100 arrivals per hour). Use a run length of 25 times.

# Bonus challenge:
# - First, try to implement this without setting a random seed
# - Then, update the method with an approach to control the randomness.

# Hints:
# - We learnt how to sample things using a numpy random number generator in the sampling
# notebook. Excluding a random seed, the basic method for drawing a single sample follows
# this pattern:
# rng = np.random.default_rng ()
# sample = rng.exponential (scale = 12.0)

# Exercise Solution

# %% [CELL 1: Imports]
import numpy as np

# %% [CELL 2: RNG generator]
# Without seed
# rng = np.random.default_rng ()

# With seed
rng = np.random.default_rng (60)

# %% [CELL 2: Arrival generator]
def arrivals_generator (env):
    while True:        
        samples = rng.exponential (scale = 0.6)
        inter_arrival_time = samples
        yield env.timeout (inter_arrival_time)
        print (f'poison arrives at: {env.now}')

# %% [CELL 3: Simulation runs]
RUN_LENGTH = 25
env = simpy.Environment ()
env.process (arrivals_generator (env))
env.run (until = RUN_LENGTH)
print (f'end of simulation run. clock time = {env.now}')











# %%
