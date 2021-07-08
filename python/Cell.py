## Cell.py
## Ford Fishman
## 6/24/21

import numpy as np

class Cell():

    def __init__(self, ty:str=None, trait:float=None, R:float=None, mt:float=None, g:float=None, size:float=None) -> None:
        """ 
        Cell - basic individual unit
        ----------------------------
        ty (str): type or allele of cell (Default: None)
        trait (float): primary trait value (Default: None)
        R (float): endogenous resources
        size (float): cell size
        """
        assert ty in ['A', 'B', None], "ty should be A or B"
        assert trait is None or trait >= 0 and trait <= 1, "trait should be on interval [0,1]"

        self.req = set(['C'])
        self.type = self.init_ty(ty)
        self.init_traits(trait, R, mt, g, size)
        
        # self.mt = 0.5 # cost of self maintenance
        # self.g = 0.4 # growth constant
        self.rp = 0.1 # resource production constant 
        # self.supplement()
        self.d = 0.01 # base probability of dormancy
        self.isDepleted = False
        self.isDividing = False

    def init_ty(self, ty) -> str:
        """  
        Initialize cell type
        """
        if ty is None: # default behavior, else return provided value
            
            ty = np.random.choice(['A', 'B'])

            if ty=='A': self.req.add('B')
            elif ty=='B': self.req.add('A')
            
        return ty
    
    def initialize(self,x):
        
        if x is None:
            y = np.random.uniform()
        
        else:
            y = x

        return y
    
    def init_traits(self, trait, R, mt, g, size, mutate=False) -> None:
        """ 
        picks a random trait value if not specified 
        """
        self.trait = self.initialize(trait)
        self.R = self.initialize(R)
        self.mt = self.initialize(mt)
        self.g = self.initialize(g)
        self.size = self.initialize(size)
        # self.trait = 1 # for testing
        
        if mutate:
            pass 

        return None
    
    def depleted(self) -> None:
        self.isDepleted = self.R <= 0
        # if self.R <= 0: print('empty')
        return None

    def maintenance(self) -> None:
        self.R -= min(self.R, self.mt)
        return None
    
    def growth(self) -> None:
        g = min(self.g, self.R)
        self.R -= g
        self.size += g
        return None
    
    def division(self) -> None:
        if self.R > 0:
            
            p = self.R/(1+self.R) * self.size/(1+self.size) # probability of cell division

            if np.random.binomial(1, p) == 1:
                self.isDividing = True

        return None

    def divide(self) -> None:

        self.size /= 2
        self.R /= 2
        self.isDividing = False 

        return None
        
    def produce(self) -> float:
        # s = self.trait*self.R
        s = self.trait
        return max(s, 0)
    
    def uptake(self, resource) -> None:
        """  
        Intake resources
        """

        self.R += resource

        return None
    
    
    def dorm(self) -> None:
        """ 
        calculate probability of going dormant
        prob = 0 if the cell is dividing
        """

        if not self.isDividing:
            self.d = 1/(1+self.R)
        
        else:
            self.d = 0

        return None
    
    # def production(self, resources:dict):
    #     """  
    #     Amount of secondary resource this cell produces
    #     """

    #     return self.trait * self.fitness(resources)

    # def supplement(self) -> None:
    #     """  
    #     Required resources for the cell
    #     Current version is basic
    #     """
    #     self.sup = set()

    #     if self.type=='A':
    #         self.sup.add('R_a')

    #     elif self.type=='B':
    #         self.sup.add('R_b')

    #     return None
    
    # def fitness(self, resources:dict) -> float:
    #     """
    #     Absolute fitness W of cell based on available resources
    #     """
    #     req = self.req

    #     # initialize
    #     W = 0 
    #     W_req = 0 # required
    #     W_sup = 0 # supplemental

    #     for resource, R in resources.items(): # for all  resources

    #         if resource in req:  # if required
    #             W_req *= R/(50 + R)
        
    #         elif True: # if supplemental

    #             W_sup *= R/(50 + R)


    #     if W_req==0: 
            
    #         W = 0 # if no required resources, can't grow 
        
    #     else:
    #          W = W_req + W_sup

    #     return W

        