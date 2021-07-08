from matplotlib.pyplot import subplot
import numpy as np
from copy import deepcopy
from Cell import Cell

class Population():
    """ 
    Population - collection of cells
    --------------------------------
    cells (list) - list of Cell() objects
    N (int, default=100) - population size 
    """
    def __init__(self, cells:list, resources:dict, N:int=100) -> None:
        # try
        self.update(cells)
        self.dormant = list()
        self.resources = resources  

    def timestep(self) -> None:
        """
        Processes that occur every timestep 
        """

        # 1 resuscitate
        resc = self.resc()
        cells = np.array(self.cells + resc) # bank of cells comes prev timestep and current resuscitated cells

        if len(cells) < 1: # if there are no active cells
            return None

        # 2 internal cell processes

        m = 1


        order = np.random.choice(range(self.N), size=self.N) # randomize order of cells

        for i in order:

            cell = cells[i]

            cell.maintenance()
            cell.growth()

            # resource production
            R = cell.produce()
            cell.R -= R
            self.resources[cell.type] += R

            cell.division()
            

            for r in cell.req: # for all resources this cell uses

                if self.resources[r] >= m:

                    cell.R += m
                    self.resources[r] -= m

            cell.depleted()
                  
        
        # 3 pick next gen
        cells = np.array(cells) # convert for slicing
        
        # cells without resources die
        notDepleted = np.array([not cell.isDepleted for cell in cells])
        cells = cells[notDepleted]

        if len(cells) < 1: # second check for active cells
            return None

        isDividing = np.array([cell.isDividing for cell in cells])
        daughters = [self.daughterCell(cell) for cell in cells[isDividing]]

        next_gen = list(cells) + daughters
        
        # 4 dormancy
        # dorm = self.dorm()
        # self.dormant += dorm # add cells to dormancy list
        self.update(next_gen)
        

        for resource, R in self.resources.items():
            if R <= 0:
                self.resources[resource] = 0

        return None

    def freq(self, ty) -> float:
        """
        Returns frequency of given allele (ty) in pop  
        """
        return self.types.count(ty)/len(self.cells)
    
    def density(self, ty) -> int:
        """
        Returns frequency of given allele (ty) in pop   
        """
        return self.types.count(ty)

    def trait_mean(self, ty = None) -> float:
        """
        Takes mean trait of pop 
        """
        mu = 0

        if ty is None:
            
            mu = np.mean(self.traits)
        
        else:
            subpop = self.subpop(ty)

            if len(subpop) > 0 :
                traits = [cell.trait for cell in subpop]
                mu = np.mean(traits)

        return mu
    
    def R(self, ty:str=None) -> float:
        """  
        """
        R = 0

        if ty is None:

            R = np.mean([cell.R for cell in self.cells])
        
        else:
            subpop = self.subpop(ty)
            if len(subpop) > 0 :
                R = np.mean([cell.R for cell in subpop])

        return R
    
    def subpop(self, ty:str):
        """
        Selects cells of a specific type  
        """
        return [cell for cell in self.cells if cell.type == ty]
    
    def daughterCell(self, cell:Cell)->Cell:
        cell.divide()
        daughter = deepcopy(cell)
        return daughter
    
    def dorm(self, responsive:bool=False) -> list:
        """ 
        Select cells to enter dormancy
        """
        cells = self.cells
        
        if responsive:
            # pD = np.array([ cell.d for cell in cells ]) # array of dormancy probabilities
            pD = np.array([ cell.d for cell in cells ]) # array of dormancy probabilities
            rng = np.random.uniform(size = self.N) # cell becomes dormant if random num is smaller than pD
            isDormant = pD > rng  
            dormant = np.array(cells)[isDormant] # filter by the cells that should be dormant

        else:
            pD = 0.01 # per cell probability of going dormant
            N = len(cells)
            D = np.random.binomial( n=N, p=pD ) # the number of cells that go into dormancy is binomially distributed
            dormant = np.random.choice(cells, size=D, replace=False) # pick which cells go dormant

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
    
    def update(self, cells) -> None:
        """ update population attributes """
        self.types = [cell.type for cell in cells]
        self.traits = np.array([cell.trait for cell in cells])
        self.cells = cells
        self.N = len(cells)
        return None

    # def weights(self, cells, resources) -> np.array:
    #     """ 
    #     Return probabilities that each cell is selected for the next timestep
    #     """
    #     W = [ cell.fitness(resources) for cell in cells ] # absolute fitness for all

    #     sumW = np.sum(W)

    #     if sumW == 0:
    #         return None

    #     weights = W/np.sum(W) # relative fitness, kinda
        
    #     if np.isnan(np.sum(weights)):
    #         weights = None

    #     return weights