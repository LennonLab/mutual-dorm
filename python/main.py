import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Cell import Cell
from Population import Population
import plots
from copy import deepcopy
import multiprocessing as mp

### arguments ###
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', default='.', type=str, help="Desired name of output path")
parser.add_argument('-S','--sims', default=10, type=int, help="Number of simulations to run (--single must be False)")
parser.add_argument('-t','--timesteps', default=100, type=int, help="Number of timesteps in each simulation")
parser.add_argument('-st','--stoch', dest='resp', action='store_false', help='Stochastic dormancy mode')
parser.add_argument('-R','--react', dest='resp', action='store_true', help='Reactive dormancy mode')
parser.add_argument('-nd', dest='dorm', action='store_false', help='Deactivates dormancy')
parser.add_argument('-es', '--estoch', dest='estoch', action='store_true', help='enables environmental stochasticity')
parser.add_argument('-C','--cells', default=2, type=int, help='number of cell types (1 or 2)')
parser.add_argument('-a', default=0, type=float, help="Starting density of resource A")
parser.add_argument('-b', default=0, type=float, help="Starting density of resource B")
parser.add_argument('-c', default=100, type=float, help="Starting density of resource C")
parser.add_argument('-n', default=100, type=int, help="Starting total cell density")
parser.add_argument('-tr','--trait', default=None, type=float, help="Mutualistic trait value")
parser.add_argument('-r','--resources', default=None, type=float, help="Initial internal cell resource concentration")
parser.add_argument('-mt', default=None, type=float, help="Maintenance cost per timestep")
parser.add_argument('-g', '--growth',default=None, type=float, help="Growth per timestep")
parser.add_argument('-sz', '--size',default=None, type=float, help="Initial cell size")
parser.add_argument('-des','--description', default='', type=str, help="Short description of the the run that will go into the logfile.")

# set defaults for boolean arguments
parser.set_defaults(resp=True)
parser.set_defaults(dorm=True)
parser.set_defaults(estoch=False)

# Read in command line arguments
arguments = parser.parse_args()
out = arguments.output
sims = arguments.sims
t_max = arguments.timesteps
responsive = arguments.resp
dorm = arguments.dorm
env_stoch = arguments.estoch
num_cells = arguments.cells
A = arguments.a
B = arguments.b
C = arguments.c 
N = arguments.n
trait = arguments.trait
R = arguments.resources
mt = arguments.mt
g = arguments.growth
size = arguments.size
description = arguments.description

assert num_cells in {1,2}, "Number of cells should be 1 or 2"

# create dictionary of parameters
params = {'num_cells':num_cells, 'N':N, 'A':A, 'B':B, 'C':C, 'responsive':responsive, 'dorm':dorm,'trait':trait, 'R':R, 'mt':mt, 'g':g, 'size':size}


### initialize simulation ###

def init_pop(num_cells:int=2, N:int=N, A:float=A, B:float=B, C:float=C, responsive:bool=responsive, dorm:bool=dorm,trait:float=trait, R:float=R, mt:float=mt, g:float=g, size:float=size, **kwargs):
    """
    Returns a pop with the specified features
    """
    cell_type = None

    if num_cells==1:

        cell_type = 'A'

    R_i = {
        'A': A,
        'B': B,
        'C': C
    }

    cell_args = {
        'ty': cell_type,
        'trait': trait,
        'R': R,
        'mt': mt,
        'g': g,
        'size': size
    }

    pop = Population([ Cell(**cell_args) for i in range(N) ], R_i, responsive=responsive, dorm=dorm)

    return pop

### trackers ###

def init_containers(env_stoch, **kwargs):
    pop = init_pop(**kwargs)

    freqA = [pop.freq('A')]
    mean_trait = [pop.trait_mean()]
    trait_a = [pop.trait_mean('A')]
    trait_b = [pop.trait_mean('B')]
    D = [len(pop.dormant)]
    Na = [pop.density('A')]
    Nb = [pop.density('B')]
    r_a = [pop.resources['A']]
    r_b = [pop.resources['B']]
    r_c = [pop.resources['C']]
    R = [pop.R()]
    Ra = [pop.R('A')]
    Rb = [pop.R('B')]
    mean_Na = [pop.density('A')]
    mean_Nb = [pop.density('B')]

    containers = [pop, freqA, mean_trait, trait_a, trait_b, D, Na, Nb, r_a, r_b, r_c, R, Ra, Rb, env_stoch, mean_Na, mean_Nb]
    return containers

# runs a single simulation
def sim(containers):
    pop, freqA, mean_trait, trait_a, trait_b, D, Na, Nb, r_a, r_b, r_c, R, Ra, Rb, env_stoch, mean_Na, mean_Nb = containers

    if env_stoch: # environmental stochasticity mode
        C_flow = [0, 0, 0, 0, 100]
    
    else: 
        C_flow = [100]

    for t in range(t_max): # for each timestep

        pop.timestep()
        pop.resources['C'] += np.random.choice(C_flow)

        # store values 
        R.append(pop.R())
        Ra.append(pop.R('A'))
        Rb.append(pop.R('B'))
        
        freqA.append(pop.freq('A'))
        Na.append(pop.density('A'))
        Nb.append(pop.density('B'))
        mean_trait.append(pop.trait_mean())
        trait_a.append(pop.trait_mean('A'))
        trait_b.append(pop.trait_mean('B'))
        D.append(len(pop.dormant))
        r_a.append(pop.resources['A'])
        r_b.append(pop.resources['B'])
        r_c.append(pop.resources['C'])
        mean_Na.append(np.mean(Na))
        mean_Nb.append(np.mean(Nb))

    return [pop, freqA, mean_trait, trait_a, trait_b, D, Na, Nb, r_a, r_b, r_c, R, Ra, Rb, mean_Na, mean_Nb]

# run multiple simulations
def multisims(sims:int=sims, params:dict=params, env_stoch:bool=env_stoch):

    map_containers = [init_containers(env_stoch,**params) for i in range(sims)] # initialized simulations

    pool = mp.Pool(mp.cpu_count()) # parallel setup

    results = pool.map(sim, map_containers, chunksize=1) # run simes
    
    # store results
    freqs = [result[1][-1] for result in results] # list of the last freq of each sim
    traits = [result[2][-1] for result in results] 
    metabolites = [result[8][-1]+result[9][-1] for result in results] 
    Rs = [result[11][-1] for result in results] 
    Ns = [result[6][-1]+result[7][-1] for result in results]
    mean_Ns = [result[-1][-1]+result[-2][-1] for result in results]

    # plot output
    plots.freq_m(out+'frequencies.png',freqs)
    plots.trait_m(out+'traits.png', traits)
    plots.meta_m(out+'metabolites.png', metabolites)
    plots.R_m(out+'resources.png', Rs)
    plots.N_m(out+'densities.png', Ns)
    plots.mean_N_m(out+'mean_densities',mean_Ns)

    # save .csv
    df = pd.DataFrame(
        {
            'freqs': freqs,
            'traits': traits,
            'metabolites': metabolites,
            'resources': Rs,
            'density': Ns
        }
    )

    df.to_csv(out+'summary.csv')

    return None

### execute ###
if __name__ == "__main__":

    print("Description\n%s" % description)
    
    if sims > 1: # if we are running more than one simulation
        multisims(sims=sims, params=params)

        print('Environmental Stochasticity:\t%s' % env_stoch)

        for param, val in params.items():

            print("%s:\t%s" % (param, val))
                
    
    else:
        pass