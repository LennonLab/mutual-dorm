
from cc3d.core.PySteppables import *
import numpy as np

class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self,frequency)

    def start(self):
        
        self.track_cell_level_scalar_attribute(field_name='conc', attribute_name='conc')

        for cell in self.cell_list:

            cell.targetVolume = 20
            cell.lambdaVolume = 20.0
            cell.dict['conc'] = np.random.uniform()
            cell.dict['growth'] = 0.1
            cell.dict['mt'] = 0.05
            # cell.targetLength = 3
            # cell.lambdaLength = 20.0
            
        
        
class GrowthSteppable(SteppableBasePy):
    def __init__(self,frequency=1):
        SteppableBasePy.__init__(self, frequency)

  
        
class MitosisSteppable(MitosisSteppableBase):
    def __init__(self,frequency=1):
        MitosisSteppableBase.__init__(self,frequency)
    
    def start(self):
        self.plot_win = self.add_new_plot_window(title='Cell Density',
                                                 x_axis_title='MonteCarlo Step (MCS)',
                                                 y_axis_title='Density', x_scale_type='linear', y_scale_type='linear',
                                                 grid=False)
        
        self.plot_win.add_plot("A", style='Dots', color='blue', size=1)
        self.plot_win.add_plot("B", style='Dots', color='green', size=1)
        self.plot_win.add_plot("DA", style='Dots', color='red', size=1)
        self.plot_win.add_plot("DB", style='Dots', color='yellow', size=1)

    def step(self, mcs):
        
        # arguments are (name of the data series, x, y)
        self.plot_win.add_data_point("A", mcs, len(self.cell_list_by_type(self.A)))
        self.plot_win.add_data_point("B", mcs, len(self.cell_list_by_type(self.B)))
        self.plot_win.add_data_point("DA", mcs, len(self.cell_list_by_type(self.DA)))
        self.plot_win.add_data_point("DB", mcs, len(self.cell_list_by_type(self.DB)))
        
        cells_to_divide=[]
        secretorA = self.get_field_secretor("A")
        secretorB = self.get_field_secretor("B")
        secretorC = self.get_field_secretor("C")
        
        
        
        for cell in self.cell_list_by_type(self.B, self.A):
            
            # arguments are: cell, max uptake, relative uptake
            
            c = secretorC.uptakeInsideCellTotalCount(cell, 1.0, 0.1)
            
            # R = abs(c.tot_amount)
            
            if cell.type == self.A: 
                b = secretorB.uptakeInsideCellTotalCount(cell, 1.0, 0.1) # A uses b
                secretorA.secreteOutsideCellAtBoundary(cell, 0.1) # A secretes a
                R = abs(c.tot_amount) + abs(b.tot_amount)
                # R = 3
            
            if cell.type == self.B: 
                a = secretorA.uptakeInsideCellTotalCount(cell, 1.0, 0.1)# B uses a
                secretorB.secreteOutsideCellAtBoundary(cell, 0.1) # B secretes b                          
                R = abs(c.tot_amount) + abs(a.tot_amount)
                # R = 3
                
                   
            
            # print(r.tot_amount)
            cell.dict['conc'] += R
            cell.targetVolume += cell.dict['growth'] * cell.dict['conc']
            
            cell.dict['conc'] -= cell.dict['growth'] * cell.dict['conc'] + cell.dict['mt']
          
            # print(cell.dict['conc'])
            
            # cell death
            if cell.dict['conc'] <= 0.0:

                cell.targetVolume=0
                cell.lambdaVolume=100
                continue
            
            # dormancy
            # stochastic
            # d = 0.01
            
            # responsive
            d = 1/(10+cell.dict['conc'])
            
            if np.random.uniform() < d:
                
                if cell.type == self.A: 
                    cell.type = self.DA
                elif cell.type == self.B: 
                    cell.type = self.DB
                    
                cell.targetVolume = 5
                cell.lambdaVolume = 100
                continue
            

        
            if cell.volume>40:
                cells_to_divide.append(cell)
                print('divide')

        for cell in cells_to_divide:

            self.divide_cell_random_orientation(cell)
            # Other valid options
            self.divide_cell_orientation_vector_based(cell,1,1,0)
            self.divide_cell_along_major_axis(cell)
            self.divide_cell_along_minor_axis(cell)
        
        # dormant cells
        
        for cell in self.cell_list_by_type(self.DA, self.DB):
            # resuscitations
            if np.random.uniform() < 0.01:
                if cell.type == self.DA: 
                    cell.type = self.A
                elif cell.type == self.DB: 
                    cell.type = self.B
                # cell.targetVolume = 20
                cell.lambdaVolume = 20.0
                continue
            
            # decay
            
            if np.random.uniform() < 0.01:

                cell.targetVolume = 0
                cell.lambdaVolume = 100
        

    def update_attributes(self):
        # reducing parent target volume
        self.parent_cell.targetVolume /= 2.0    
        self.parent_cell.dict['conc'] /= 2.0        

        self.clone_parent_2_child()            

        # for more control of what gets copied from parent to child use cloneAttributes function
        # self.clone_attributes(source_cell=self.parent_cell, target_cell=self.child_cell, no_clone_key_dict_list=[attrib1, attrib2]) 
        
        # if self.parent_cell.type==1:
            # self.child_cell.type=2
        # else:
            # self.child_cell.type=1

       

        