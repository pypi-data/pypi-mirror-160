#from Tkinter import *
import numpy as np
from copy import *

# *************************************************************************
# Interface IVisit_ParameterSet and IVisit_Simulation:
# Provides Structure for a simulation that can be controlled by IVisit 
# *************************************************************************
class IVisit_Parameters:        # Example Struct of Simulation parameters (are referred to via database objects Parameter.name)
    par1 = 1                           # int parameter
    par2 = 2.5                         # float parameter
    par3 = 'flag_on'                   # text parameter

class IVisit_Data:              # Example Struct of Data Fields to be displayed (that are referred to via database objects DataArray.name)
    data1 = np.array([1])              # single int data
    data2 = np.array([2.2])            # single float data
    data3 = ['textdata']               # single text data
    data4 = np.array([[1,2],[3,4]])    # numerical data matrix

class IVisit_Simulation:        # derive your simulation from this class (do not forget to call the constructor!!!!)
    def __init__(self,name_arg="IVisitSimulation1", parameters_arg=IVisit_Parameters, data_arg=IVisit_Data, updateMode='sync'):
        """
        :param updateMode: if updateMode=='sync' then parameter widgets (e.g., sliders) are written to simulation only before call to step()
                           othersie (updateMode=='async') parameter widgets are written through to simulation immediately after changes
        """
        # store name, parameters, data fields
        self.name=name_arg
        self.parameters=parameters_arg
        self.data=data_arg
        self.updateMode=updateMode
        # create a parameter dictionaries of the simulation parameter and simulation data
        self.parameters_dict          = self.get_dict_of_parameters()           # get working copy of the parameters
        self.parameters_dict_original = self.get_dict_of_parameters(1) # get a deep copy to retain original parameter values (during initializiation)
        # create a dictionary of the simulation data attributes
        self.data_dict = self.get_dict_of_data()             # get copy of data (no deep copy) containing references to the simulation data                                                                                        
        self.display=None
        
    def get_dict_of_parameters(self,flagDeepCopy=0,parameters=None):    # returns a dict of the (self.)parameters
        if parameters==None: parameters=self.parameters
        pars_dict=vars(parameters)                                                                             # basic dict of attributes of the parameter struct
        pars_dict={k:pars_dict[k] for k in pars_dict.keys() if not(k.startswith('__') and k.endswith('__'))}   # refine (to keep only the real simulation parameters) 
        if flagDeepCopy>0:
            pars_dict = {k:deepcopy(pars_dict[k]) for k in pars_dict.keys()}                                   # make a deep copy of all attributes (to preserve lists etc.)
        return pars_dict

    def get_dict_of_data(self,flagDeepCopy=0,data=None):                # returns a dict of the (self.)data
        if data==None: data=self.data
        data_dict=vars(data)                                                                                   # basic dict of attributes of the data struct
        data_dict={k:data_dict[k] for k in data_dict.keys() if not(k.startswith('__') and k.endswith('__'))}   # refine (to keep only the real simulation data) 
        if flagDeepCopy>0:
            data_dict = {k:deepcopy(data_dict[k]) for k in data_dict.keys()}                                   # make a deep copy of all attributes (to preserve lists etc.)
        return data_dict

    def set_dict_of_parameters(self,pars_dict=None):      # set parameters with the values of pars_dict 
        if pars_dict==None: pars_dict=self.parameters_dict
        self.parameters_dict=pars_dict
        for k in pars_dict:
            setattr(self.parameters,k,pars_dict[k])

    def print_parameters(self,pars=None,indent=""):
        if(pars==None): pars=self.parameters
        allpars=vars(pars)         
        allpars={k:allpars[k] for k in allpars.keys() if not(k.startswith('__') and k.endswith('__'))}
        for k in allpars.keys():
            print(str(indent)+"Parameter '"+str(k)+"': "+str(allpars[k]))

    def print_data(self,data=None,indent=""):
        if(data==None): data=self.data
        alldata=vars(data)         
        alldata={k:alldata[k] for k in alldata.keys() if not(k.startswith('__') and k.endswith('__'))}
        for k in alldata.keys():
            print(str(indent)+"Data field '"+str(k)+"': "+str(alldata[k]))

    def print_state(self):
        print("IVisit_Simulation "+str(self.name)+":")
        print("   parameters = "+str(self.parameters))
        print("   data       = "+str(self.data))
        print("   parameters_dict          = "+str(self.parameters_dict))
        print("   parameters_dict_original = "+str(self.parameters_dict_original))
        print("   data_dict  = "+str(self.data_dict))
        print("   Parameter Struct = ...")
        self.print_parameters(indent="      ")
        print("   Data Struct = ...")
        self.print_data(indent="      ")

    def main_init(self):      # main init procedure (to initialize/booting by start...)
        pass

    def init(self):           # init a new simulation run (but keep allocated data)
        pass

    def bind(self,parent=None,display=None):  # bind events to the simulation; parent is typcially the ivisit object (having a display object where to bind to)
        pass

    def step(self):           # one simulation step
        pass

# ****************************************************************************************************************************

if __name__ == '__main__':
    print("\nModule test of ivisit.simulation.py")
    print("--------------------------------------\n") 

    class MyParameters:
        par1 = 1                     # int parameter
        par2 = 2.5                   # float parameter
        par3 = 'flag_on'             # text parameter
        size = 100;                  # size of matrix
        listpar = [6,8,9]            # list parameter
        listpar2 = [1,2,3]           # another list parameter
        
    class MyData:              # Example Struct of Data Fields to be displayed (that are referred to via database objects DataArray.name)
        data1 = np.array([1])              # single int data
        data2 = np.array([2.2])            # single float data
        data3 = ['textdata']               # single text data
        data4 = np.array([[1,2],[3,4]])    # numerical data matrix
        mat = np.array([[1,2],[3,4]])      # another data matrix 

    class MySimulation(IVisit_Simulation):
        def __init__(self,name_arg="MySimulation1",parameters_arg=MyParameters,data_arg=MyData):
            IVisit_Simulation.__init__(self,name_arg,parameters_arg,data_arg)

        def main_init(self): pass          # or further stuff...

        def init(self): pass               # or further stuff...

        def step(self): 
            p=self.parameters
            self.mat = np.random.rand(p.size,p.size)  # generate random matrix

    sim1 = MySimulation("MySimulation1",MyParameters,MyData)
    sim1.main_init()
    sim1.init()
    sim1.step()
    sim1.print_state()
    
    # do a parameter change (as may be done by ivisit)
    pars=sim1.get_dict_of_parameters()
    pars['par1']=1000
    pars['listpar']=[100,101,102]
    pars['listpar2'][0]=10000
    sim1.set_dict_of_parameters(pars)

    print("\nState after parameter changes:")
    sim1.print_state()

