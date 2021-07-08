import numpy as np
from Cell import Cell
from Population import Population

N_i = 100 # initial N
t_max = 1000

R_i = {
    'A': 0,
    'B': 0,
    'C': 100
}
pop = Population([ Cell() for i in range(N_i) ], R_i)

freqA = [pop.freq('A')]
mean_trait = [pop.trait_mean()]
D = [len(pop.dormant)]
Na = [pop.density('A')]
Nb = [pop.density('B')]
r_a = [R_i['A']]
r_b = [R_i['B']]
r_c = [R_i['C']]
R = [np.mean([cell.R for cell in pop.cells])]

for i in range(t_max):

    pop.timestep()

    R.append(np.mean([cell.R for cell in pop.cells]))

    pop.resources['C'] += 100
    
    freqA.append(pop.freq('A'))
    Na.append(pop.density('A'))
    Nb.append(pop.density('B'))
    mean_trait.append(pop.trait_mean())
    D.append(len(pop.dormant))
    r_a.append(pop.resources['A'])
    r_b.append(pop.resources['B'])
    r_c.append(pop.resources['C'])

