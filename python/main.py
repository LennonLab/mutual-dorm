import matplotlib.pyplot as plt
import numpy as np
from Cell import Cell
from Population import Population
from copy import deepcopy


### initialize simulation ###

def init_pop(N:int=100, A:float=0, B:float=0, C:float=100, responsive:bool=False, trait:float=None, R:float=None, mt:float=None, g:float=None, size:float=None):
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

pop = init_pop(responsive=True)
t_max = 1000

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

### simulate ###

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


### plot ###


# densities over time