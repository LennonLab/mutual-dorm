import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# parameters
N = 100
t_max = 100

# population
trait = np.random.choice(['A', 'B'], size=N, replace=True)
population = pd.DataFrame(trait)
pop = trait

# output
output_dict = {
    "generations":range(0,t_max),
    "p":np.zeros(t_max)}

output = pd.DataFrame(output_dict)

output.loc[0, 'p'] = sum(pop=="A")/N

# simulate

for t in range(1,t_max):
    prev_pop = pop # parent generation

    pop = np.random.choice(prev_pop, size=N, replace=True) # random proliferation

    output.loc[t,'p'] = sum(pop=="A")/N

fig, ax = plt.subplot()
