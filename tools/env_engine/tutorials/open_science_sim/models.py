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

# Model 4: COLLECTING RESULTS FROM A SINGLE RUN:
# When running our DES, we want to collect data that helps us to analyse the system performance,
# such as wait times, resource utilisation, and queue lengths.
# a tool like simpy allows you to collect your data flexibly using an approach that makes sense to you!
# Some options are:

# 1. Store process metrics during a run and perform calculations at the end of a run.
# For example, if you want to calculate mean patient waiting time then store each patient waiting time
# in a list and calculate the mean at the end of the run

# 2. Code an auditor / observer process. This process will periodically observe the state of the system.
# We can use this to collect information on current state at time t. For example, how many patients
# are queueing and how many have a call in progress by time of day.

# 3. Conduct an audit or calculate running statistics as the simulation executes an event. For example,
# as a patient completes a call we can calculate a running mean of waiting times and a running total
# of the operators are taking calls. The latter measure can then be used to calculate server utilisation.
# You could also use this approach to audit queue length where the queue length is recorded each time
# request for a resource is made (and / or when a resource is released).

# This notebook provides an example of the first strategy

# %% [CELL 1: Imports]
import simpy
import numpy as np
import itertools

# CALCULATING MEAN WAITING TIME:
# The second strategy to results collections is to store either a reference to a quantitative value
# (e.g. waiting time) during the run. Once the run is complete you will need to include a procedure
# for computing the metric of interest.

# - An advantage of this strategy is that it is very simple, captures all data, and has minimal
# computational overhead during a model run!

# - A potential disadvantage is that for complex simulation you may end up storing large amounts
# of data in memory. In these circumstances, it may be worth exploring events driven strategies to
# reduce memory requirements

# In our example, we will:
# 1. Create a list (results ['waiting_times]) to store each caller's wait time
# 2. When the model runs, each time a caller enters service, the service () function will append
# a waiting_time for the caller to the list.
# 3. At the end of the run, we will loop through these references and calculate mean waiting time

# CREATE LIST TO STORE WAIT TIMES:
# our list will be stored within a python directory we create called results. This means that it is
# simple to add new metrics (e.g. utilisiation, queue length at a later date)

# The dictionary has notebook level scope. This means that any functions or class in the notebook 
# can access and / or append to the list access via the key waiting_times

# %% [CELL 2: List to store wait times]
results = {}
results['waiting_times'] = []

# ENABLE / DISABLE PRINT STATEMENTS
# Throughout the model, we use print statements to print progress (e.g. every time an operator starts
# and ends a call)

# To enable / disable printing, we create a helper function called trace () that wraps print.
# We can set a variable called TRACE to switch these print messages on or off

# %% [CELL 3: Enable / disable print statements]
def trace (msg):
    if TRACE:
        print (msg)

# SERVICE & ARRIVAL FUNCTIONS
# The only modification we need to make is to the service function. We will add in a line of code to
# record the waiting_time of the caller as they enter the service

# results['waiting times'].append (waiting_time)

# %% [CELL 4: Service function]
def service (identifier, operators, env, service_rng):
    '''
    Simulates the service process for a call operator

    1. Request and wait for a call operator
    2. Phone triage (triangular)
    3. Exit system

    Params:
    ------

    identifier: int
        A unique identifier for this caller

    operators: simpy.Resource
        The pool of call operators that answers calls

    env: simpy.Environment
        The current environment the simulation is running in
        We use this to pause and restart the process after a delay

    service_rng: numpy.random.Generator
        The random number generator used to sample service times
    '''

    start_wait = env.now

    # Request an operator
    with operators.request () as req:
        yield req
    
        # record the waiting time for call to be answered
        waiting_time = env.now - start_wait

        # MODIFICATION: store the waiting time...
        results ['waiting_times'].append (waiting_time)

        trace (f'Operator answered call {identifier} at ' \
               + f'{env.now:.3f}')
    
        # sample call duration
        call_duration = service_rng.triangular (left = 5.0, mode = 7.0,
                                                right = 10.0)
    
        # Schedule process to begin again after call_duration
        yield env.timeout (call_duration)

        # Print out information for patient
        trace (f'Call {identifier} ended {env.now:.3f}; ' \
               + f'Waiting time was {waiting_time:.3f}')

# %% [CELL 5: Arrival function]
def arrivals_generator (env, operators):
    '''
    IAT is exponentially distributed

    Params:
    ------

    env: simpy.Environment
        The simpy environment for the simulation

    operators: simpy.Resource
        The pool of call operators.
    '''
    
    # Create the arrival process rng
    arrival_rng = np.random.default_rng ()
    
    # Create the service rng that we pass to each service process created
    service_rng = np.random.default_rng ()

    # Use itertools as it provides an infinite loop
    # With a counter variable that we can use for unique IDs
    for caller_count in itertools.count (start = 1):

        # 100 calls per hour (sim time units = minutes)
        inter_arrival_time = arrival_rng.exponential (60/100)
        yield env.timeout (inter_arrival_time)

        trace (f'Call arrives at : {env.now:.3f}')

        # Create a new simpy process for serving this caller
        # We pass in the caller id, the operator resources, env, and the rng
        env.process (service (caller_count, operators, env, service_rng))


# CONDUCT A SINGLE RUN OF THE MODEL
# We could keep the code to run the model as a script. However, it is useful to create a new function
# called single_run that we use to perform a single replication of the model and return results

# If we later want to run multiple replications it is just a case of running  single_run in a loop

# We add a line of code to find the mean waiting times from results.

# %% [CELL 5: Single run function]
def single_run (run_length, n_operators):
    '''
    Perform a single replication of the simulation model and
    return the mean waiting time as a result

    Params:
    ------

    run_length: float
        The duration of the simulation run in minutes

    n_operators: int
        The number of call operators to create as a resource

    Returns:
    -------

    mean_waiting_time: int
    '''

    env = simpy.Environment ()
    operators = simpy.Resource (env, capacity = n_operators)

    env.process (arrivals_generator (env, operators))
    env.run (until = run_length)
    print (f'End of run. Simulation clock time = {env.now}')

    # Calculate results on notebook level variables
    mean_waiting_time = np.mean (results ['waiting_times'])

    return mean_waiting_time

# %% [CELL 6: Running the model]
results = {}
results ['waiting_times'] = []

# Model params
RUN_LENGTH = 1000
N_OPERATORS = 13

# Turn off caller level results
TRACE = False

mean_waiting_time = single_run (RUN_LENGTH, N_OPERATORS)
print ("Simulation Complete")
print (f"Waiting time for call operators: {mean_waiting_time:.2f} minutes") 
