#!/usr/bin/python
# -*- coding: utf-8-unix -*-

from supy.sqldatabase import *



##################################################################################################################################################################
##################################################################################################################################################################
#        
# Define Databases for Studbase (see UML CHART design_ivisit.dia/pdf)     
#        
##################################################################################################################################################################
##################################################################################################################################################################


##################################################################################################################################################################
# Table 1: Simulation: Simulation instances for simulation program that use certain parameter sets  
##################################################################################################################################################################
class tb_simulation_cfg(Table_cfg):
    name = 'simulation'
    # column definitions
    col_names           = ['key'        ,'name'    ,'comment','date_init','date_lastmod','simsteps_per_frame','frames_per_step','delay_per_step','grade'  ]
    col_types           = ['INTEGER'    ,'TEXT'    ,'TEXT'   ,'TEXT'     ,'TEXT'        ,'INTEGER'           ,'INTEGER'        ,'INTEGER'       ,'INTEGER']
    col_references      = [None         ,None      ,None     ,None       ,None          ,None                ,None             ,None            ,None     ]
    col_constraints     = ['PRIMARY KEY','NOT NULL',None     ,None       ,None          ,None                ,None             ,None            ,None     ]
    col_ref_constraints = [None         ,None      ,None     ,None       ,None          ,None                ,None             ,None            ,None     ]
    col_defaults        = [None         ,"'N.N.'"  ,"'N.N.'" ,"'N.N.'"   ,"'N.N.'"      ,1                   ,1                ,1               ,-1       ]
    indexes             = None
    # default rows (that will be stored during creation)
    rows_default     = ["(0,'N.N.','N.N.','N.N.','N.N.',1,1,1,-1)"]

##################################################################################################################################################################
# Table 2: Parameter: Parameter of the simulation program that may be influenced by IVisit   
##################################################################################################################################################################
class tb_parameter_cfg(Table_cfg):
    name = 'parameter'
    # column definitions
    col_names           = ['key'        ,'name'    ,'comment','type'  ,'range' ,'listidx']
    col_types           = ['INTEGER'    ,'TEXT'    ,'TEXT'   ,'TEXT'  ,'TEXT'  ,'INTEGER']
    col_references      = [None         ,None      ,None     , None   , None   ,None     ]
    col_constraints     = ['PRIMARY KEY','NOT NULL',None     , None   , None   ,None     ]
    col_ref_constraints = [None         ,None      ,None     , None   , None   ,None     ]
    col_defaults        = [None         ,"'N.N.'"  ,"'N.N.'" ,"'int'" ,"'N.N.'",0        ]
    indexes             = None
    # default rows (that will be stored during creation)
    rows_default     = []  #["(0,'N.N.','N.N.','int','N.N.',0)"]

##################################################################################################################################################################
# Table 3: DataArray: Data field of the simulation program (typically a numpy-array) that may be displayed by IVisit   
##################################################################################################################################################################
class tb_dataarray_cfg(Table_cfg):
    name = 'dataarray'
    # column definitions
    col_names           = ['key'        ,'name'    ,'comment','type'  ,'range' ]
    col_types           = ['INTEGER'    ,'TEXT'    ,'TEXT'   ,'TEXT'  ,'TEXT'  ]
    col_references      = [None         ,None      ,None     ,None    ,None    ]
    col_constraints     = ['PRIMARY KEY','NOT NULL',None     ,None    ,None    ]
    col_ref_constraints = [None         ,None      ,None     ,None    ,None    ]
    col_defaults        = [None         ,"'N.N.'"  ,"'N.N.'" ,"'int'" ,"'N.N.'"]
    indexes             = None
    # default rows (that will be stored during creation)
    rows_default     = [] #["(0,'N.N.','N.N.','int','N.N.')"]

##################################################################################################################################################################
# Table 4: ParameterWidget: Widget class for displaying and modifying parameters    
##################################################################################################################################################################
class tb_parameterwidget_cfg(Table_cfg):
    name = 'parameterwidget'
    # column definitions
    col_names           = ['key'        ,'key_simulation'   ,'key_parameter'    ,'name'  ,'comment','type'    ,'range'      ,'items'          ,'size'   ,'pos'    ,'value' ]
    col_types           = ['INTEGER'    ,'INTEGER'          ,'INTEGER'          ,'TEXT'  ,'TEXT'   ,'TEXT'    ,'TEXT'       ,'TEXT'           ,'TEXT'   ,'TEXT'   ,'TEXT'  ]
    col_references      = [None         ,'simulation'       ,'parameter'        ,None    ,None     ,None      ,None         ,None             ,None     ,None     ,None    ]
    col_constraints     = ['PRIMARY KEY','NOT NULL'         ,'NOT NULL'         ,None    ,None     ,None      ,None         ,None             ,None     ,None     ,None    ]
    col_ref_constraints = [None         ,'ON DELETE CASCADE','ON DELETE CASCADE',None    ,None     ,None      ,None         ,None             ,None     ,None     ,None    ]
    col_defaults        = [None         ,0                  ,0                  ,"'N.N.'","'N.N.'" ,"'slider'","'[0,1,1,1]'","'[Item1,Item2]'","'[0,0]'","'[0,0]'","'0'"   ]
    indexes             = [('idx_simulation',['key_simulation']),('idx_parameter',['key_parameter'])]
    # default rows (that will be stored during creation)
    rows_default     = []   # ["(0,0,0,'N.N.','N.N.','slider','[0,1,1,1]','[Item1,Item2]','[0,0]','[0,0]','0')"]

##################################################################################################################################################################
# Table 5: DataWidget: Widget class for displaying data    
##################################################################################################################################################################
class tb_datawidget_cfg(Table_cfg):
    name = 'datawidget'
    # column definitions
    col_names           = ['key'        ,'key_simulation'   ,'key_dataarray'    ,'name'  ,'comment','type'   ,'range' ,'pos'    ,'scale']
    col_types           = ['INTEGER'    ,'INTEGER'          ,'INTEGER'          ,'TEXT'  ,'TEXT'   ,'TEXT'   ,'TEXT'  ,'TEXT'   ,'FLOAT']
    col_references      = [None         ,'simulation'       ,'dataarray'        ,None    ,None     ,None     ,None    ,None     ,None   ]
    col_constraints     = ['PRIMARY KEY','NOT NULL'         ,'NOT NULL'         ,None    ,None     ,None     ,None    ,None     ,None   ]
    col_ref_constraints = [None         ,'ON DELETE CASCADE','ON DELETE CASCADE',None    ,None     ,None     ,None    ,None     ,None   ]
    col_defaults        = [None         ,0                  ,0                  ,"'N.N.'","'N.N.'" ,"'image'","'N.N.'","'[0,0]'",1      ]
    indexes             = [('idx_simulation',['key_simulation']),('idx_dataarray',['key_dataarray'])]
    # default rows (that will be stored during creation)
    rows_default      = []    # ["(0,0,0,'N.N.','N.N.','image','N.N.','[0,0]',1)"]

##################################################################################################################################################################
# Table 6: CommentWidget: Widget class for displaying comments    
##################################################################################################################################################################
class tb_commentwidget_cfg(Table_cfg):
    name = 'commentwidget'
    # column definitions
    col_names           = ['key'        ,'key_simulation'   ,'name'  ,'comment','type'       ,'fontname','fontsize','fontstyle','fontcolor','bgcolor','flagDisplayName','pos'    ]
    col_types           = ['INTEGER'    ,'INTEGER'          ,'TEXT'  ,'TEXT'   ,'TEXT'       ,'TEXT'    ,'INTEGER' ,'TEXT'     ,'TEXT'     ,'TEXT'   ,'INTEGER'        ,'TEXT'   ]
    col_references      = [None         ,'simulation'       ,None    ,None     ,None         ,None      ,None      ,None       ,None       ,None     ,None             ,None     ]
    col_constraints     = ['PRIMARY KEY','NOT NULL'         ,None    ,None     ,None         ,None      ,None      ,None       ,None       ,None     ,None             ,None     ]
    col_ref_constraints = [None         ,'ON DELETE CASCADE',None    ,None     ,None         ,None      ,None      ,None       ,None       ,None     ,None             ,None     ]
    col_defaults        = [None         ,0                  ,"'N.N.'","'N.N.'" ,"'textfield'","'Arial'" ,10        ,"'normal'" ,"'black'"  ,"'gray'" ,0                ,"'[0,0]'"]
    indexes             = [('idx_simulation',['key_simulation'])]
    # default rows (that will be stored during creation)
    rows_default     = ["(0,0,'N.N.','N.N.','textfield','Arial',10,'normal','black','gray',0,'[0,0]')"]


##################################################################################################################################################################
# Index dicts for easy accessing data via column names
##################################################################################################################################################################

icol_simulation      = {tb_simulation_cfg.col_names     [i]:i for i in range(len(tb_simulation_cfg.col_names))}
icol_parameter       = {tb_parameter_cfg.col_names      [i]:i for i in range(len(tb_parameter_cfg.col_names))}
icol_dataarray       = {tb_dataarray_cfg.col_names      [i]:i for i in range(len(tb_dataarray_cfg.col_names))}
icol_parameterwidget = {tb_parameterwidget_cfg.col_names[i]:i for i in range(len(tb_parameterwidget_cfg.col_names))}
icol_datawidget      = {tb_datawidget_cfg.col_names     [i]:i for i in range(len(tb_datawidget_cfg.col_names))}
icol_commentwidget   = {tb_commentwidget_cfg.col_names  [i]:i for i in range(len(tb_commentwidget_cfg.col_names))}

##################################################################################################################################################################
# Database of all Tables   
##################################################################################################################################################################

class db_ivisit_cfg(sqldatabase_cfg):
    default_filename = 'ivisit_default.db'
    table_configs = [tb_simulation_cfg, \
                     tb_parameter_cfg, \
                     tb_dataarray_cfg, \
                     tb_parameterwidget_cfg, \
                     tb_datawidget_cfg, \
                     tb_commentwidget_cfg]


##################################################################################################################################################################
##################################################################################################################################################################
# Module test
##################################################################################################################################################################
##################################################################################################################################################################

if __name__ == '__main__':
    print("\nModule test of studbase_defdb.py")
    print("------------------------------------\n") 
    db = sqldatabase(db_ivisit_cfg)
    db.print_database(1)

