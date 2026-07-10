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

# Model 3: Queueing model of a 111 call centre

# Problem background
# Call operators in an 111 (urgent care) service receive calls at a rate
# of 100 per hour. Call length can be represented by a triangular distribution.
# Calls last between 5 minutes and 15 minutes

# We'll first create a python function called service () to simulate the service
# process for a call operator. We need to include the following logic:
# 1. Request and wait (if necessary) for a call operator
# 2. Undergo phone triage (a delay). This is a sample from the Triangular distribution
# 3. Exit the system

# Each caller that arrives in the simulation will this function as a SimPy process.
# We will pass:
# - A unique patient identifier (identifier)
# - A pool of operator resources (operators)
# - The environment (env)
# - The service process random number generator object (service_rng)

# %% [CELL 1: Imports]
import simpy
import numpy as np
import itertools

# %% [CELL 2: The function]
def service (identifier, operators, env, service_rng):
    '''
    Simulates the service progress for a call operator

    1. Request and wait for a call operator
    2. Phone triage
    3. Exit system

    Params:
    ------
    
    identifier: int
        A unique identifier for this caller
        
    operators: simpy.Resource
        The pool of call operators that answer calls
        These are shared across resources

    env: simpy.Environment
        The current environment the simulation is running in
        We use this to pause and restart the process after a delay

    service_rng: numpy.random.Generator
        The random number generator used to sample service times
    '''
    start_wait = env.now
    
    with operators.request () as req:
        yield req

        waiting_time = env.now - start_wait
        print (f'Operator answered call {identifier} at {env.now:.2f}')

        call_duration = service_rng.triangular (left = 5.0, mode = 7.0, right = 10.0)
        yield env.timeout (call_duration)

        print (f'Call {identifier} ended {env.now:.2f}; ' \
               + f'waiting time was {waiting_time:.2f}')


# %% [CELL 3: Generators]
def arrivals_generator (env, operators):
    '''
    Simulates the call arrival process and spawn
    Inter-arrival time (IAT) is exponentially distributed

    Params:
    ------

    env: simpy.Environment
        The simpy environment for the simulation
    '''

    arrivals_rng = np.random.default_rng ()
    
    service_rng = np.random.default_rng ()

    for caller_count in itertools.count (start = 1):
        inter_arrival_time = arrivals_rng.exponential (60.0 / 100.0)
        yield env.timeout (inter_arrival_time)
        print (f'Call arrives at: {env.now:.2f}')

        env.process (service (caller_count, operators, env, service_rng))

# %% [CELL 4: Run the model]

# Model params
RUN_LENGTH = 100
N_OPERATORS = 13

# Create SimPy environment and operator resources
env = simpy.Environment ()
operators = simpy.Resource (env, capacity = N_OPERATORS)

env.process (arrivals_generator (env, operators))
env.run (until = RUN_LENGTH)
print (f'End of run. Simulation clock time = {env.now}')
