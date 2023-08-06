#from Tkinter import *
from ivisit.defdb import *
from ivisit.simulation import *

# ***************************************************************************
# class ParameterWidgetDef:
# GUI-independent definition of a ParameterWidget 
#    - provides all information necessary 
#      to a create a real widget that can be displayed on the working frame 
#    - A ParameterWidgetDef thereby links a Database ParameterWidget entry 
#      to the corresponding simulation parameters of the simulation program
# ***************************************************************************
class ParameterWidgetDef:     
    def __init__(self,wdefcoll_arg,pardata=None):
        self.wdefcoll          = wdefcoll_arg   # reference to WidgetDefCollection object
        self.key               = None           # key in database table ParameterWidget or DataWidget (depending on type)
        self.name              = None           # name of the widget
        self.comment           = None           # comment 
        self.type              = None           # either 'slider' or 'listsel' or 'textfield' 
        self.range             = None           # list of [min,max,nTicks,scale] 
        self.items             = None           # list of [item1,item2,...]
        self.size              = None           # [sz_x,sz_y) size of widget
        self.pos               = None           # (x,y) position of widget
        self.value             = None           # value of the parameter
        self.key_simulation    = None           # key of the simulation
        self.key_parameter     = None           # key of the parameter
        self.name_parameter    = None           # name of the parameter
        self.comment_parameter = None           # comment of the parameter
        self.type_parameter    = None           # either 'int' or 'float' or 'text'
        self.range_parameter   = None           # either [min,max] or [val1,val2,...]
        self.listidx_parameter = None           # index of parameter value to be controlled (if parameter is list)
        self.flagListParameter = None           # if set then parameter is a list
        if pardata!=None:
            self.setData(pardata)

    def setData(self,pardata):   # set attributes according to pardata (which is a join of the columns of the tables (simulation,parameterwidget,parameter))
        # (i) do raw input from tables
        icol=self.wdefcoll.icol_s_pw_p          # set reference to index dict to pardata
        self.key              =pardata[icol['pw.key']]          # key of the parameter widget
        self.name             =pardata[icol['pw.name']]         # name of the parameter widget
        self.comment          =pardata[icol['pw.comment']]      # comment 
        self.type             =pardata[icol['pw.type']]         # either 'slider' or 'listsel' or 'textfield' 
        self.range            =pardata[icol['pw.range']]        # list of [min,max,nTicks,scale]
        self.items            =pardata[icol['pw.items']]        # list of [item1,item2,...]
        self.size             =pardata[icol['pw.size']]         # [sz_x,sz_y) size of widget
        self.pos              =pardata[icol['pw.pos']]          # (x,y) position of widget
        self.value            =pardata[icol['pw.value']]        # value of the parameter
        self.key_simulation   =pardata[icol['s.key']]           # key of the simulation
        self.key_parameter    =pardata[icol['p.key']]           # key of the parameter
        self.name_parameter   =pardata[icol['p.name']]          # name of the parameter
        self.comment_parameter=pardata[icol['p.comment']]       # comment of the parameter
        self.type_parameter   =pardata[icol['p.type']]          # either 'int' or 'float' or 'text'
        self.range_parameter  =pardata[icol['p.range']]         # either [min,max] or [val1,val2,...]
        self.listidx_parameter=pardata[icol['p.listidx']]       # index of parameter value to be controlled (if >=0 and parameter is list)
        self.flagListParameter=0                                # default no list parameter
        # (ii) refined post-processing
        self.type=self.type.strip()                             # strip white space
        self.type_parameter=self.type_parameter.strip()         # strip white space
        self.range=self.wdefcoll.db.parseStringAsList(self.range,self.type_parameter,[0,1,1,1])                   # finalize self.range as list of ints or floats or strings
        self.items=self.wdefcoll.db.parseStringAsList(self.items,'string',[0,1])                                  # finalize self.items as list of strings
        self.size=self.wdefcoll.db.parseStringAsList(self.size,'int',[0,0])                                       # finalize self.size as list of ints 
        self.range_parameter=self.wdefcoll.db.parseStringAsList(self.range_parameter,self.type_parameter,[0,1])   # finalize self.range_parameter as list of ints or floats or strings
        self.pos=self.wdefcoll.db.parseStringAsList(self.pos,'int',[0,0])                                         # finalize self.pos as list of ints [x,y]
        if(self.type_parameter=='int'):
            try:
                self.value=int(self.value)
            except ValueError as e:
                print("Warning: cannot convert self.value=",self.value," to int for parameter widget with name=",self.name)
                self.value=0
                pass
        else:
            if(self.type_parameter=='float'):
                self.value=float(self.value)
        p=self.wdefcoll.getSimParameterValue(self.name_parameter,0)
        if isinstance(p, (list, tuple)): self.flagListParameter=1

    def getSimParValue(self,default_value=None):      # return current parameter value from simulation program
        p=self.wdefcoll.getSimParameterValue(self.name_parameter,default_value)
        if self.flagListParameter>0:
            assert isinstance(self.value, (list, tuple)),"Simulation parameter name_parameter="+self.name_parameter+" is neither list nor tuple, but ParameterWidgetDef "+\
                   self.name+" says flagListParameter="+str(self.flagListParameter)
            assert (self.listidx_parameter>=0)and(self.listidx_parameter<len(p),"listidx_parameter="+str(self.listidx_parameter)+" is out of allowed range >=0 and <len(p)="+str(len(p)))
            p=p[self.listidx_parameter]
        else:
            assert not isinstance(self.value, (list, tuple)),"Simulation parameter name_parameter="+self.name_parameter+" is list or tuple, but ParameterWidgetDef "+\
                   self.name+" says flagListParameter="+str(self.flagListParameter)
        return p

    def setSimParValue(self):                         # write parameter value to simulation program 
        if(self.flagListParameter):
            p=self.wdefcoll.getSimParameterValue(self.name_parameter,default_value)   # get reference to simulation parameter list
            assert isinstance(p, (list, tuple)),"Simulation parameter name_parameter="+self.name_parameter+" is neither list nor tuple, but ParameterWidgetDef "+\
                   self.name+" says flagListParameter="+str(self.flagListParameter)
            assert (self.listidx_parameter>=0)and(self.listidx_parameter<len(p)),"listidx_parameter="+str(self.listidx_parameter)+" is out of allowed range >=0 and <len(p)="+str(len(p))
            p[self.listidx_parameter]=self.value
        else:
            self.wdefcoll.setSimParameterValue(self.name_parameter,self.value) 
        
    def saveWidgetDataToDatabase(self):              # save the parameter value and position from widgetdef (that may have been manipulated in GUI) to database
        self.wdefcoll.db.simple_update_byPKEY('parameterwidget',['value','pos'],[str(self.value),str(self.pos)],['key'],[str(self.key)])

    def printState(self,indent=""):
        print(indent+"ParameterWidgetDef "+str(self.name)+" :")
        print(indent+"   key               ="+str(self.key))
        print(indent+"   comment           ="+str(self.comment))
        print(indent+"   type              ="+str(self.type))
        print(indent+"   range             ="+str(self.range))
        print(indent+"   items             ="+str(self.items))
        print(indent+"   size              ="+str(self.size))
        print(indent+"   pos               ="+str(self.pos))
        print(indent+"   value             ="+str(self.value))
        print(indent+"   key_simulation    ="+str(self.key_simulation))
        print(indent+"   key_parameter     ="+str(self.key_parameter))
        print(indent+"   name_parameter    ="+str(self.name_parameter))
        print(indent+"   comment_parameter ="+str(self.comment_parameter))
        print(indent+"   type_parameter    ="+str(self.type_parameter))
        print(indent+"   range_parameter   ="+str(self.range_parameter))
        print(indent+"   listidx_parameter ="+str(self.listidx_parameter))
        print(indent+"   flagListParameter ="+str(self.flagListParameter))
        print(indent+"   data_value        ="+str(self.type))

# ***************************************************************************
# class DataWidgetDef:
# GUI-independent definition of a DataWidget 
#    - provides all information necessary 
#      to a create a real widget that can be displayed on the working frame 
#    - A DataWidgetDef thereby links a Database DataWidget entry 
#      to the corresponding simulation DataArrays of the simulation program
# ***************************************************************************
class DataWidgetDef:     
    def __init__(self,wdefcoll_arg,datadata=None):
        self.wdefcoll          = wdefcoll_arg   # reference to WidgetDefCollection object
        self.key               = None           # key of the data widget
        self.name              = None           # name of the data widget
        self.comment           = None           # comment 
        self.type              = None           # either 'image' or 'textfield' 
        self.range             = None           # list of [min,max] 
        self.pos               = None           # (x,y) position of widget
        self.scale             = None           # scale of the data widget 
        self.data              = None           # reference to the data object (typically a numpy array)
        self.key_simulation    = None           # key of the simulation
        self.key_dataarray     = None           # key of the dataarray
        self.name_dataarray    = None           # name of the dataarray
        self.comment_dataarray = None           # comment of the dataarray
        self.type_dataarray    = None           # either 'int' or 'float' or 'binary' or 'text'
        self.range_dataarray   = None           # [min,max] 
        self.flagRefData       = None           # if flag>0 then self.data is a reference (to an array); otherwise it is a non-referential data (e.g.,an integer)
        if datadata!=None:
            self.setData(datadata)

    def setData(self,datadata):   # set attributes according to datadata (which is a join of the columns of the tables (simulation,datawidget,dataarray))
        # (i) do raw input from tables
        icol=self.wdefcoll.icol_s_dw_da          # set reference to index dict to datadata
        self.key              =datadata[icol['dw.key']]        # key of the data widget
        self.name             =datadata[icol['dw.name']]       # name of the data widget
        self.comment          =datadata[icol['dw.comment']]    # comment 
        self.type             =datadata[icol['dw.type']]       # either 'image' or 'textfield' 
        self.range            =datadata[icol['dw.range']]      # list of [min,max] 
        self.pos              =datadata[icol['dw.pos']]        # (x,y) position of widget
        self.scale            =datadata[icol['dw.scale']]      # scale of the data widget 
        self.data             =None                            # reference to the data object (typically a numpy array)
        self.key_simulation   =datadata[icol['s.key']]         # key of the simulation
        self.key_dataarray    =datadata[icol['da.key']]        # key of the dataarray
        self.name_dataarray   =datadata[icol['da.name']]       # name of the dataarray
        self.comment_dataarray=datadata[icol['da.comment']]    # comment of the dataarray
        self.type_dataarray   =datadata[icol['da.type']]       # either 'int' or 'float' or 'binary' or 'text'
        self.range_dataarray  =datadata[icol['da.range']]      # list of [min,max] 
        self.flagRefData      =0                               # default no ref parameter 
        # (ii) refined post-processing
        self.type=self.type.strip()                            # strip white space
        self.type_dataarray=self.type_dataarray.strip()        # strip white space
        self.range=self.wdefcoll.db.parseStringAsList(self.range,self.type_dataarray,[0,1])                      # finalize self.range as list of ints or floats 
        self.range_dataarray=self.wdefcoll.db.parseStringAsList(self.range_dataarray,self.type_dataarray,[0,1])  # finalize self.range_parameter as list of ints or floats or strings
        self.pos=self.wdefcoll.db.parseStringAsList(self.pos,'int',[0,0])                                        # finalize self.pos as list of ints [x,y]
        self.scale=float(self.scale)                           # convert to float
        self.setDataFromSimulation(0)                          # set self.data by simulation data
        self.flagRefData=0                                     # test if self.data has reference-type (1) or not (0)
        if isinstance(self.data, (list, tuple, np.ndarray)):   # ditto...
            self.flagRefData=1

    def setDataFromSimulation(self,default_value=None):        # get current simulation data from simulation program and set self.data accordingly
        self.data=self.wdefcoll.getSimData(self.name_dataarray,default_value)

    def saveWidgetDataToDatabase(self):              # save the widget position from widgetdef (that may have been manipulated in GUI) to database
        self.wdefcoll.db.simple_update_byPKEY('datawidget',['pos'],[str(self.pos)],['key'],[str(self.key)])

    def printState(self,indent=""):
        print(indent+"DataWidgetDef "+str(self.name)+" :")
        print(indent+"   key               ="+str(self.key))
        print(indent+"   comment           ="+str(self.comment))
        print(indent+"   type              ="+str(self.type))
        print(indent+"   range             ="+str(self.range))
        print(indent+"   pos               ="+str(self.pos))
        print(indent+"   scale             ="+str(self.scale))
        print(indent+"   data              ="+str(self.data))
        print(indent+"   key_simulation    ="+str(self.key_simulation))
        print(indent+"   key_dataarray     ="+str(self.key_dataarray))
        print(indent+"   name_dataarray    ="+str(self.name_dataarray))
        print(indent+"   comment_dataarray ="+str(self.comment_dataarray))
        print(indent+"   type_dataarray    ="+str(self.type_dataarray))
        print(indent+"   range_dataarray   ="+str(self.range_dataarray))
        print(indent+"   flagRefData       ="+str(self.flagRefData))


# ***************************************************************************
# class CommentWidgetDef:
# GUI-independent definition of a CommentWidget 
#    - provides all information necessary 
#      to a create a real widget that can be displayed on the working frame 
#    - Note that a CommentWidgetDef is not linked to a database entry! 
# ***************************************************************************
class CommentWidgetDef:     
    def __init__(self,wdefcoll_arg,comdata=None):
        self.wdefcoll          = wdefcoll_arg   # reference to WidgetDefCollection object
        self.key               = None           # key of the comment widget
        self.name              = None           # name of the comment widget
        self.comment           = None           # comment 
        self.type              = None           # either 'textfield' or ??? 
        self.fontname          = None           # fontname (e.g., Arial)  
        self.fontsize          = None           # fontsize (e.g., 10)
        self.fontstyle         = None           # fontstyle (e.g., Normal)  
        self.fontcolor         = None           # fontcolor (e.g., black) 
        self.flagDisplayName   = None           # if flag=1 then display name on frame; if flag=0 then do not display
        self.pos               = None           # (x,y) position of widget
        self.key_simulation    = None           # key of the simulation
        if comdata!=None:
            self.setData(comdata)

    def setData(self,comdata):   # set attributes according to comdata (which is a join of the columns of the tables (simulation,datawidget,dataarray))
        # (i) do raw input from tables
        icol=self.wdefcoll.icol_s_cw          # set reference to index dict to comdata
        self.key              =comdata[icol['cw.key']]             # key of the comment widget
        self.name             =comdata[icol['cw.name']]            # name of the comment widget
        self.comment          =comdata[icol['cw.comment']]         # comment 
        self.type             =comdata[icol['cw.type']]            # either 'image' or 'textfield' 
        self.fontname         =comdata[icol['cw.fontname']]        # fontname (e.g., Arial)  
        self.fontsize         =comdata[icol['cw.fontsize']]        # fontsize (e.g., 10)
        self.fontstyle        =comdata[icol['cw.fontstyle']]       # fontstyle (e.g., Normal)  
        self.fontcolor        =comdata[icol['cw.fontcolor']]       # fontcolor (e.g., black) 
        self.flagDisplayName  =comdata[icol['cw.flagDisplayName']] # if flag=1 then display name on frame; if flag=0 then do not display
        self.pos              =comdata[icol['cw.pos']]             # (x,y) position of widget
        self.key_simulation   =comdata[icol['s.key']]              # key of the simulation
        # (ii) refined post-processing
        self.type=self.type.strip()                                # strip white space
        self.fontsize=int(self.fontsize)                           # convert to int
        self.flagDisplayName=int(self.flagDisplayName)             # convert to int
        self.pos=self.wdefcoll.db.parseStringAsList(self.pos,'int',[0,0]) # finalize self.pos as list of ints [x,y]

    def saveWidgetDataToDatabase(self):              # save the widget position from widgetdef (that may have been manipulated in GUI) to database
        self.wdefcoll.db.simple_update_byPKEY('commentwidget',['pos'],[str(self.pos)],['key'],[str(self.key)])

    def printState(self,indent=""):
        print(indent+"CommentWidgetDef "+str(self.name)+" :")
        print(indent+"   key               ="+str(self.key))
        print(indent+"   comment           ="+str(self.comment))
        print(indent+"   type              ="+str(self.type))
        print(indent+"   fontname          ="+str(self.fontname))
        print(indent+"   fontsize          ="+str(self.fontsize))
        print(indent+"   fontstyle         ="+str(self.fontstyle))
        print(indent+"   fontcolor         ="+str(self.fontcolor))
        print(indent+"   flagDisplayName   ="+str(self.flagDisplayName))
        print(indent+"   pos               ="+str(self.pos))
        print(indent+"   key_simulation    ="+str(self.key_simulation))


# *********************************************************************
# *********************************************************************
# class IVisitWidgetDefCollection:
# Collection of widget definitions, e.g., read from a ivisit database
#
# The purpose of this class is to link database widget objects to 
# their corresponding simulation entities (like parameters and data) 
# *********************************************************************
# *********************************************************************
class IVisitWidgetDefCollection:
    def __init__(self, db_arg, sim_arg):
        # connect to database and simulation program
        self.db  = db_arg     # Reference to IVisit database
        self.sim = sim_arg    # Reference to simulation object (having a field 'parameters')
        self.simpars=self.sim.parameters_dict  # reference to working copy of the simulation parameters
        self.simpars_original=self.sim.parameters_dict_original # reference to (deep) copy of the original simulation parameters (as defined in class struct IVisit_Parameters)
        self.dataarrays = self.sim.data_dict # reference to data fields of the simulation program
        # simulation key and name (refers to database table 'simulation')
        self.simulation_key = None  # simulation.key
        self.simulation_name = ""   # simulation.name
        # simulation control parameters        
        self.simulation_simsteps_per_frame = 1    # number of simulation steps per displayed frame (i.e., #Felix steps per call to interface step() 
        self.simulation_frames_per_step    = 1    # number of display frames per call to onStep()  
        self.simulation_delay_per_step     = 1    # delay (in msec) per call to self.onStep() (e.g., after run or cont)
        # dicts for easy access of table columns
        self.icol_s=icol_simulation
        l1,l2,l3=['s.'+c for c in tb_simulation_cfg.col_names], ['pw.'+c for c in tb_parameterwidget_cfg.col_names], ['p.'+c for c in tb_parameter_cfg.col_names]
        l=l1+l2+l3
        self.icol_s_pw_p={l[i]:i for i in range(len(l))}    # e.g., icol_s_pw_p['pw.key'] is index of parameterwidget.key within join of simulation,parameterwidget,parameter
        l2,l3=['dw.'+c for c in tb_datawidget_cfg.col_names], ['da.'+c for c in tb_dataarray_cfg.col_names]
        l=l1+l2+l3
        self.icol_s_dw_da={l[i]:i for i in range(len(l))}   # e.g., icol_s_dw_da['dw.key'] is index of datawidget.key within join of simulation,datawidget,dataarray
        l4=['cw.'+c for c in tb_commentwidget_cfg.col_names]
        l=l1+l4
        self.icol_s_cw={l[i]:i for i in range(len(l))}      # e.g., icol_s_dw_da['dw.key'] is index of datawidget.key within join of simulation,datawidget,dataarray
        # very database (list of IVisitWidgetDef objects)
        self.wdefs_parameters = []     # list of all ParameterWidget definitions
        self.wdefs_data       = []     # list of all DataWidget definitions
        self.wdefs_comments   = []     # list of all CommentWidget definitions

    def initFromDatabase(self,sim_key):    # create and initialize all widgetdefs from the database for simulation with key sim_key
        # (i) read in data of simulation table
        res = self.db.simple_select('*','simulation',where='key='+str(sim_key))[0]
        self.simulation_key               =res[icol_simulation['key']]
        self.simulation_name              =res[icol_simulation['name']]
        self.simulation_comment           =res[icol_simulation['comment']]
        self.simulation_date_init         =res[icol_simulation['date_init']]
        self.simulation_date_lastmod      =res[icol_simulation['date_lastmod']]
        self.simulation_simsteps_per_frame=res[icol_simulation['simsteps_per_frame']]
        self.simulation_frames_per_step   =res[icol_simulation['frames_per_step']]
        self.simulation_delay_per_step    =res[icol_simulation['delay_per_step']]
        # (ii) read in parameter widgets
        joinon_clause = ['parameterwidget.key_simulation=simulation.key','parameterwidget.key_parameter=parameter.key']
        res = self.db.simple_select('*',['simulation','parameterwidget','parameter'],joinon=joinon_clause,where='simulation.key='+str(sim_key))
        self.wdefs_parameters = [ParameterWidgetDef(self,d)   for d in res]
        # (iii) read in data widgets
        joinon_clause = ['datawidget.key_simulation=simulation.key','datawidget.key_dataarray=dataarray.key']
        res = self.db.simple_select('*',['simulation','datawidget','dataarray'],joinon=joinon_clause,where='simulation.key='+str(sim_key))
        self.wdefs_data = [DataWidgetDef(self,d)   for d in res]
        # (iv) read in comment widgets
        joinon_clause = ['commentwidget.key_simulation=simulation.key']
        res = self.db.simple_select('*',['simulation','commentwidget'],joinon=joinon_clause,where='simulation.key='+str(sim_key))
        self.wdefs_comments = [CommentWidgetDef(self,d)   for d in res]

    def saveToDatabase(self):  # save all data from widgetdefs (that may have been manipulated by GUI) to database 
        for wdef in self.wdefs_parameters: wdef.saveWidgetDataToDatabase()
        for wdef in self.wdefs_data      : wdef.saveWidgetDataToDatabase()
        for wdef in self.wdefs_comments  : wdef.saveWidgetDataToDatabase()

    def getSimParameterValue(self,parname,default_value=None):    # get simulation parameter value from simulation program
        try:
            p=getattr(self.sim.parameters,parname)
        except AttributeError as e:
            if(default_value!=None):
                p=default_value
                print("Warning: AttributeError in IVisitWidgetDefCollection.getSimParameterValue(...): parameter with parname=",parname,\
                      " seems not to exist in simulation program (simpars=",self.simpars,")! Returning default_value=",default_value) 
                p=default_value
            else:
                raise e
        return p

    def setSimParameterValue(self,parname,value):                # set simulation parameter value in simulation program
        try:
            p=setattr(self.sim.parameters,parname,value)
        except AttributeError as e:
            print("Error: AttributeError in IVisitWidgetDefCollection.setSimParameterValue(...): parameter with parname=",parname,\
                  " seems not to exist in simulation program (simpars=",self.simpars,")! Returning default_value=",default_value) 
            raise e

    def getSimData(self,dataarray_name,default_value=None):      # get simulation data field from simulation program
        try:
            d=getattr(self.sim.data,dataarray_name)
            #print("getSimDAta, dataarray_name=",dataarray_name," d=",d)
        except AttributeError as e:
            if(default_value!=None):
                d=default_value
                print("Warning: AttributeError in IVisitWidgetDefCollection.getSimData(...): Data array with dataarray_name=",dataarray_name,\
                      " seems not to exist in simulation program (datarrays=",self.dataarrays,")! Returning default_value=",default_value) 
                d=default_value
            else:
                raise e
        #print("finally: getSimDAta, dataarray_name=",dataarray_name," d=",d)
        return d

    def setAllSimulationParameters(self):   # write all parameter values to simulation program 
        for pw in self.wdefs_parameters:    # loop over all parameter widgets
            pw.setSimParValue()             # write parameter value to simulation program 

    def setAllSimulationDataArrays(self):   # get all data arrays from simulation program and write to data widgets  
        for dw in self.wdefs_data:          # loop over all data widgets
            dw.setDataFromSimulation()      # get data from simuation program and write to data widget  

    def printState(self):
        print("IVisitWidgetDefCollection "+self.db.filename+":")
        print("   Simulation Program sim.name   = ",self.sim.name)
        print("   simulation_key                = ",self.simulation_key)
        print("   simulation_name               = ",self.simulation_name)
        print("   simulation_simsteps_per_frame = ",self.simulation_simsteps_per_frame)
        print("   simulation_frames_per_step    = ",self.simulation_frames_per_step)
        print("   simulation_delay_per_step     = ",self.simulation_delay_per_step)
        print("   There are "+str(len(self.wdefs_parameters))+" parameter widgets:")
        for pw in self.wdefs_parameters: pw.printState("   ") 
        print("   There are "+str(len(self.wdefs_data))+" data widgets:")
        for dw in self.wdefs_data: dw.printState("   ") 
        print("   There are "+str(len(self.wdefs_comments))+" comment widgets:")
        for cw in self.wdefs_comments: cw.printState("   ") 
        
'''
        colnames = tb_parameterwidget ['ParameterWidget.key','ParameterWidget.name','ParameterWidget.comment','Parameter
        self.db.simple_select(['Parameter'])

        fh=open(fname,'r')
        state=0        # 0=try to read simulationfilename; 1=try to read widget definition; 2=try to read widget def parameter
        entry=PyFeWidgetDef()
        parlist_name = []
        parlist_val  = []
        newdb=PyFeWidgetDefDatabase()
        while(1) :
            line = fh.readline()
            if ((not line)or(line.isspace()))and(state==2):
                state=1
                entry.parameter_names = parlist_name
                entry.parameter_values = parlist_val
                newdb.db.append(entry)
                entry=PyFeWidgetDef()
            if not line:
                break
            if line.isspace():
                continue
            s=line.split()
            s=self.removeComments(s)      # ignore comments
            if len(s)==0:            # was the line only comments?
                continue
            if state==0:
                # scan simulation_name   felixsteps_per_frame   frames_per_step   delay_per_step
                assert (len(s)<=4)and(len(s)>=1), "ParseError: Expected simulation_name  felixsteps_per_frame frames_per_step delay_per_step"
                newdb.simulation=s[0]
                if(len(s)>1): newdb.felixsteps_per_frame=int(s[1])
                if(len(s)>2): newdb.frames_per_step=int(s[2])
                if(len(s)>3): newdb.delay_per_step=int(s[3])
                state=1
                continue
            if state==1:
                # scan basic widget definition
                assert len(s)==4, "ParseError: Expected widget definitions (data_name widget_type posx posy)"
                entry.data_name=s[0]
                entry.widget_type=s[1]
                entry.pos = (int(s[2]),int(s[3]))
                state=2
                parlist_name=[]
                parlist_val=[]
                continue
            if state==2:
                # scan widget definition parameter
                assert len(s)==2, "Parse Error: Expected widget definition parameter (parameter_name parameter_value)"
                parlist_name.append(s[0])
                parlist_val.append(s[1])
        # after end-of-file, state should be 1!!!
        assert state==1, "Parse error: Unexpected end of file " + fname 
        self.simulation = newdb.simulation
        self.db         = newdb.db

    def writeToFile(self,fname):
        fh=open(fname,'w')
        fh.write(self.simulation+"\n")
        fh.write("\n")
        for entry in self.db:
            fh.write(entry.data_name + " " + entry.widget_type + " " + str(entry.pos[0]) + " " + str(entry.pos[1]) + "\n")
            assert len(entry.parameter_names)==len(entry.parameter_values), "lists of parameter names and values must have same length!"
            for i in range(len(entry.parameter_names)):
                fh.write("   "+entry.parameter_names[i]+" "+entry.parameter_values[i]+"\n")
            fh.write("\n")
            
    def printPyFeWidgetDefDatabase(self): # print database
        print "PyFeWidgetDefDatabase (size=%i): " % len(self.db)
        print "Simulation = ", self.simulation
        for entry in self.db: 
            print "data_name =", entry.data_name, "  widget_type =", entry.widget_type, "  pos_x =", entry.pos[0], "  pos_y =", entry.pos[1]
            assert len(entry.parameter_names)==len(entry.parameter_values), "lists of parameter names and values must have same length!"
            for i in range(len(entry.parameter_names)):
                print "parameter_name =", entry.parameter_names[i], "  parameter_value =", entry.parameter_values[i]

'''

if __name__ == '__main__':
    print("\nModule test of ivisit.widgetcollection.py")
    print("-------------------------------------------\n") 
    db = sqldatabase(db_ivisit_cfg)
    sim=IVisit_Simulation()
    wdefcoll = IVisitWidgetDefCollection(db,sim)
    wdefcoll.initFromDatabase(0)
    wdefcoll.printState()

    s1='[1,2.51,3,4,5]'
    print("s1=",s1," list of int = ",db.parseStringAsList(s1,'int'))
    print("s1=",s1," list of float = ",db.parseStringAsList(s1,'float'))
    s2="[1,2.51,'3',4,'5']"
    print("s2=",s2," list of string = ",db.parseStringAsList(s1,'string'))

    #db.print_database(1)

    #fname="../example/exampleSS.gui"
    #print("Connecting to default database")
    #db = PyFeWidgetDefDatabase()
    #db.readFromFile(fname)
    #db.printPyFeWidgetDefDatabase()
    #db.writeToFile(fname+".bak")    
    
