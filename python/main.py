import argparse
import matplotlib.pyplot as plt
import numpy as np
from Cell import Cell
from Population import Population
from copy import deepcopy
import multiprocessing as mp

### arguments ###
parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', default='.', type=str, help="Desired name of output path")
parser.add_argument('-S','--sims', default=10, type=int, help="Number of simulations to run (--single must be False)")
parser.add_argument('-t','--timesteps', default=100, type=int, help="Number of timesteps in each simulation")
parser.add_argument('-S','--stoch', dest='resp', action='store_false', help='Stochastic dormancy mode')
parser.add_argument('-R','--react', dest='resp', action='store_true', help='Reactive dormancy mode')
parser.add_argument('-a', default=0, type=float, help="Starting density of resource A")
parser.add_argument('-b', default=0, type=float, help="Starting density of resource B")
parser.add_argument('-c', default=100, type=float, help="Starting density of resource C")
parser.add_argument('-n', default=0, type=int, help="Starting total cell density")
parser.add_argument('-tr','--trait', default=None, type=float, help="Mutualistic trait value")
parser.add_argument('-r','--resources', default=None, type=float, help="Initial internal cell resource concentration")
parser.add_argument('-mt', default=None, type=float, help="Maintenance cost per timestep")
parser.add_argument('-g', '--growth',default=None, type=float, help="Growth per timestep")
parser.add_argument('-sz', '--size',default=None, type=float, help="Initial cell size")


parser.set_defaults(stoch=True)

arguments = parser.parse_args()
out = arguments.output
sims = arguments.sims
t_max = arguments.timesteps
responsive = arguments.resp
A = arguments.a
B = arguments.b
C = arguments.c 
N = arguments.N
trait = arguments.trait
R = arguments.resources
mt = arguments.mt
g = arguments.growth
size = arguments.size

params = {'N':N, 'A':A, 'B':B, 'C':C, 'responsive':responsive, 'trait':trait, 'R':R, 'mt':mt, 'g':g, 'size':size}


### initialize simulation ###

def init_pop(N:int=N, A:float=A, B:float=B, C:float=C, responsive:bool=responsive, trait:float=trait, R:float=R, mt:float=mt, g:float=g, size:float=size, **kwargs):
    """
    Returns a pop with the specified features
    """
    
    R_i = {
        'A': A,
        'B': B,
        'C': C
    }

    cell_args = {
        'trait': trait,
        'R': R,
        'mt': mt,
        'g': g,
        'size': size
    }

    pop = Population([ Cell(**cell_args) for i in range(N) ], R_i, responsive=responsive)

    return pop

### trackers ###

def init_containers(**kwargs):
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

    containers = [pop, freqA, mean_trait, trait_a, trait_b, D, Na, Nb, r_a, r_b, r_c, R, Ra, Rb]
    return containers

def sim(containers):
    pop, freqA, mean_trait, trait_a, trait_b, D, Na, Nb, r_a, r_b, r_c, R, Ra, Rb = containers

    for t in range(t_max):

        pop.timestep()
        pop.resources['C'] += 100

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

    return [pop, freqA, mean_trait, trait_a, trait_b, D, Na, Nb, r_a, r_b, r_c, R, Ra, Rb]


def multisims(sims:int=sims, params:dict=params):

    map_containers = [init_containers(**params) for i in range(sims)]

    pool = mp.Pool(mp.cpu_count())

    results = pool.map(sim, map_containers, chunksize=1)

    return None




### simulate ###




### plot ###


# densities over time