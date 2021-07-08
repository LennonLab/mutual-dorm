import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

class Cell():

    def __init__(self, ty:str=None, trait:float=None, ident:str=None) -> None:
        """ 
        Cell - basic individual unit
        ----------------------------
        ty (str): type or allele of cell (Default: None)
        trait (float): primary trait value (Default: None)
        """
        assert ty in ['A', 'B', None], "ty should be A or B"
        assert trait is None or trait >= 0 and trait <= 1, "trait should be on interval [0,1]"

        self.type = self.init_ty(ty)
        self.id = ident
        self.trait = self.init_trait(trait)
        self.required()
        self.d = 0.01 # base probability of dormancy

    def init_ty(self, ty) -> str:
        """  
        Initialize cell type
        """
        if ty is None: # default behavior, else return provided value
            
            ty = np.random.choice(['A', 'B'])
            
        return ty
    
    def init_trait(self, trait, mutate=False) -> float:
        """ 
        picks a random trait value if not specified 
        """
        if trait is None: # default behavior, else return provided value

            trait = np.random.uniform()
        
        elif mutate:
            pass

        return trait
    
    def required(self) -> None:
        """  
        Required resources for the cell
        Current version is basic
        """
        self.req = set()

        if self.type=='A':
            self.req.add('R_a')

        elif self.type=='B':
            self.req.add('R_a')

        return None
    
    def fitness(self, resources:dict):
        """
        Absolute fitness W of cell based on available resources
        """
        req = self.req

        W = 0 # initialize

        for R in req: # for all required resources

            W += resources[R]            

        return W
    
    def dorm(self, resources:dict):
        """ 
        THIS NEEDS SOME WORK
        """

        req = self.req

        Rs = 0

        for R in req: # for all required resources

            Rs += resources[R]
        
        d = d + (1-Rs)

        return d


class Population():
    """ 
    Population - collection of cells
    --------------------------------
    cells (list) - list of Cell() objects
    N (int, default=100) - population size 
    """
    def __init__(self, cells:list, N:int=100) -> None:
        # try
        self.__update(cells)
        self.dormant = list()

    def timestep(self, resources) -> None:
        """
        Processes that occur every timestep 
        """
        
        cells = self.cells + self.resc() # bank of cells comes prev timestep and current resuscitated cells
        weights = self.weights(cells, resources)
        new_cells = list(np.random.choice(cells, size=self.N, replace=True, p=weights))
        self.dormant += self.dorm() # add cells to dormancy list
        self.__update(new_cells)

        return None

    def freq(self, ty) -> float:
        """
        Returns frequency of given allele (ty) in pop  
        """
        return self.types.count(ty)/len(self.cells)

    def trait_mean(self) -> float:
        """
        Takes mean trait of pop 
        """
        return np.mean(self.traits)
    
    def weights(self, cells, resources) -> np.array:
        """ 
        Return probabilities that each cell is selected for the next timestep
        """
        W = [ cell.fitness(resources) for cell in cells ] # absolute fitness for all
        
        weights = W/np.sum(W) # relative fitness, kinda
        
        return weights
    
    def dorm(self) -> list:
        """ 
        Select cells to enter dormancy
        """
        cells = self.cells
        pD = np.array([ cell.d for cell in cells ]) # array of dormancy probabilities
        rng = np.random.uniform(size = self.N) # cell becomes dormant if random num is smaller than pD
        isDormant = pD > rng  
        dormant = np.array(cells)[isDormant] # filter by the cells that should be dormant

        # pD = 0.01 # per cell probability of going dormant
        # N = len(cells)
        # D = np.random.binomial( n=N, p=pD ) # the number of cells that go into dormancy is binomially distributed
        # dormant = np.random.choice(cells, size=D, replace=False) # pick which cells go dormant

        for cell in dormant: # remove dormant cells from active population
            self.cells.remove(cell)

        return list(dormant)
    
    def resc(self) -> list:
        """
        Pick cells to resuscitate from dormancy
        """
        pR = 0.01 # per cell prob of resuscitating
        D = len(self.dormant) # number of dormant cells
        R = np.random.binomial( n=D, p=pR )
        resc = np.random.choice(self.dormant, size=R, replace=False)

        for cell in resc: # remove resuscitated cells from dormant population
            self.dormant.remove(cell)

        return list(resc)
    
    def __update(self, cells) -> None:
        """ update population attributes """
        self.types = [cell.type for cell in cells]
        self.traits = np.array([cell.trait for cell in cells])
        self.cells = cells
        self.N = len(cells)
        return None


N_i = 100 # initial N
R_a = 0 # resource conc. for type A
R_b = 0 # resource conc. for type B
pop = Population([ Cell() for i in range(N_i) ])

freqA = [pop.freq('A')]
mean_trait = [pop.trait_mean()]
D = [len(pop.dormant)]

for i in range(100):

    resources = { # resources equal to frequency of producer
        'R_b': pop.freq('A'),
        'R_a': pop.freq('B')
    }

    pop.timestep(resources)
    
    freqA.append(pop.freq('A'))
    mean_trait.append(pop.trait_mean())
    D.append(len(pop.dormant))

