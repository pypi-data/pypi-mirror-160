#!/usr/bin/python
# -*- coding: utf-8-unix -*-

from supy.sqlforms import *
from supy.sqltableeditor import *
from ivisit.defdb import *

##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
#        
# Define Dialogs for Studbase (to edit databases defined in studbase_defdb)      
#        
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################


##################################################################################################################################################################
##################################################################################################################################################################
#        
# Part I: Base class configuration of dialog widgets 
#        
##################################################################################################################################################################
##################################################################################################################################################################

##################################################################################################################################################################
# I.1: Single-Choice Listbox 
##################################################################################################################################################################
class lb_singlechoice_cfg(SQLListboxForm_config):
    # class fields from SQLListbox_config
    tables = None
    join_on = None
    cols   = None
    cols_format = None
    cols_sortbutton = None
    cols_sortbutton = None
    where = None
    where_init = None
    labeltext = None
    colvals2str = colvals2str_default
    sep = ' | '
    width = 45
    height = 10
    lbfont = ('courier',12,'normal')
    callback_select = callback_select_default
    mode_multiselect = False
    # class fields from SQLListboxForm_config
    button_str = ['Ok','Abbrechen']
    title      = 'SQLListboxForm...'  # is used only for askSQLListboxForm

##################################################################################################################################################################
# I.2: Multi-Choice Listbox 
##################################################################################################################################################################
class lb_multichoice_cfg(lb_singlechoice_cfg): 
    mode_multiselect = True

##################################################################################################################################################################
# I.3: SQL Input Form SupySQLForm_config
##################################################################################################################################################################
class form_cfg(SupySQLForm_config):
    tables                = None
    join_on               = None
    cols                  = None
    cols_type             = None
    cols_ref              = None
    cols_readonly         = None
    cols_label            = None
    cols_label_pos        = None
    cols_label_width      = 20     # may also be list
    cols_label_anchor     = 'w'    # may also be list
    cols_pos              = None
    cols_size             = 40     # may also be list
    cols_helptext         = None
    cols_browsebutton_pos = None
    select_cols           = None
    select_vals           = None
    help_event            = "<Button-3>"
    help_title            = "Hilfe"
    help_buttonname       = "Schließen"
    browse_buttonname     = "Auswählen"
    checkResults          = SupySQLForm_checkResults_default  # function to check if inputs are valid (see SupySQLForm_checkResults_default)
    update_tables         = None                              # tables to be updated after form submission
    update_tables_pkeys   = None                              # for each table (to be updated) a list of primary keys 
    update_tables_cols    = None                              # for each table (to be updated) a list of columns to be updated
 
##################################################################################################################################################################
# I.4: SQL Table Editor Input Form SupySQLForm_config
##################################################################################################################################################################
class tbed_config(SQLTableEditor_config):
    cfg_choiceLB         = None               # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm          = None               # configuration for record form (typically a SupySQLForm_config)
    align_widgets        = 'horizontal'       # either 'vertical' or 'horizontal' for alignment of listbox and form
    lbButtons_str        = ['Neu', 'Kopieren', 'Löschen']            # text for listbox buttons
    recFormButtons_str   = ['Zurücksetzen', 'Standardwerte', 'Bestätigen']       # text for form buttons
    ctrlRadioButtons_str = ['Nur anschauen', 'Verändern']                     # text for radiobuttons (read-only, write/edit option)
    ctrlButtons_str      = ['Bestätigen & Schließen', 'Abbrechen & Schließen'] # text for control buttons
    text_showinfo_cannot_delete_readonly = ("Information", "Datensatz kann nicht gelöscht werden! Nur Lese-Zugriff erlaubt!")
    text_askyesno_delete = ("Datensatz löschen?", "Wollen Sie den folgenden Datensatz wirklich löschen? \nDatensatz : ")
    # extend tbed_.... to get a valid initialization of a new record that is conditioned on exam.key (because examofcourse has no direct link to exam)
    ntom_init_on_new     = None    # list of [col_to_be_initialized,col_initialized_by,where_cond]
    

##################################################################################################################################################################
# I.5: RefNtoM Simple Listbox/Textframe 
##################################################################################################################################################################
class ntm_simple(SupySQLntomTextFrame_cfg,lb_singlechoice_cfg):
    readonly=True
    title      = None 
    ntom_flagSimple = True                   # invoke only listbox form 
    ntom_callback=editSQLTable_ntom_simple
    ntom_table1,ntom_key1=None,None          # master table and key
    ntom_table2,ntom_key2=None,None          # slave table and key
    ntom_tablenm,ntom_tablenm_cols=None,None # in order primary key, key name of table 1, key name of table 2 
    link_ntom_listbox_cfg=None               # multi-choice listbox config
    ntom_copy_cascade = None                 # define which columns of the mn-table to cascade-copy     

##################################################################################################################################################################
# I.6: RefNtoM Non-Simple Listbox/Textframe 
##################################################################################################################################################################
class ntm_nonsimple(SupySQLntomTextFrame_cfg,lb_singlechoice_cfg):
    readonly=True
    title      = None 
    ntom_flagSimple = False               # invoke only listbox form 
    ntom_callback=editSQLTables
    link_ntom_form_cfg=None               # multi-choice listbox config
    ntom_copy_cascade = None              # define which columns of the mn-table to cascade-copy     


##################################################################################################################################################################
##################################################################################################################################################################
#        
# Part II: Dialog definitions of Basic Isolated Tables  
#        
##################################################################################################################################################################
##################################################################################################################################################################

##################################################################################################################################################################
# Dialoge für Table 1: Simulation: Simulation instances for simulation program that use certain parameter sets   
##################################################################################################################################################################
class lb_simulation_cfg(lb_singlechoice_cfg):    # Listbox zur Auswahl des Datensatzes
    tables = ['simulation']
    cols   = ['simulation.key', 'simulation.name', 'date_init', 'date_lastmod', 'grade']
    cols_format = ['5d','15s:15','10s:10','10s:10','5d']
    cols_sortbutton = ['ID','Simulation','create date','last modified','grade']
    title      = 'Choose Simulation Instance'
    width=60

class form_simulation_cfg(form_cfg):            # Eingabform
    tables                = ['simulation']
    join_on               = None 
    cols                  = ['simulation.key','simulation.name','simulation.comment','simulation.date_init','simulation.date_lastmod'  ,\
                             'simulation.simsteps_per_frame'   ,'simulation.frames_per_step'               ,'simulation.delay_per_step','simulation.grade']   
    cols_type             = ['str'           ,'str'            ,'textfield'         ,'str'                 ,'str'                      ,\
                             'str'                             ,'str'                                      ,'str'                      ,'str'             ]
    cols_size             = [40              ,40               ,(40,10)             ,10                    ,10                         ,\
                             10                                ,10                                         ,10                         ,10                ]   
    cols_ref              = None 
    cols_readonly         = [1               ,0                ,0                   ,0                     ,0                          ,\
                             0                                 ,0                                          ,0                          ,0                 ]
    cols_label            = ['ID'            ,'Simulation'     ,'Comment'           ,'Date (creation)'     ,'Date (last mod)'          ,\
                             'Simsteps/Frame'                  ,'Frames/Step'                              ,'Delay/Step'               ,'Grade'           ] 
    cols_label_pos        = None
    cols_helptext         = ['ID of Simulation (integer)', 'Name of the simulation', 'comment on the simulation', 'date of creation of this simulation file', 'date of last modification',\
                             'Number of Simulation Steps per Display Frame','Number of Display Frames per IVisit call to step()','Delay [msec] per IVisit call to step()',\
                             'Grade of the Simulation, that is, an evaluation of the performance of the simulation program with the associated set of parameters']
    select_cols           = ['simulation.key']
    select_vals           = [0]                                      # default value seems irrelevant here (overwritten by tableditor...)
    update_tables = ['simulation']                                   # tables to be updated after form submission
    update_tables_pkeys = [['simulation.key']]                       # for each table (to be updated) a list of primary keys 
    update_tables_cols  = [['simulation.name','simulation.comment','simulation.date_init','simulation.date_lastmod',\
                            'simulation.simsteps_per_frame','simulation.frames_per_step','simulation.delay_per_step','simulation.grade']] # for each table (to be updated) a list of columns to be updated
    title      = 'Edit Simulation Instance ...'                   # is used only for askSupySQLForm

class tbed_simulation_cfg(tbed_config):        # Tabellenbearbeitung
    table_cfg          = tb_simulation_cfg     # table to be edited, first column is assumed to be primary key of type INTEGER!!!
    pkeys_readonly     = [0]                   # records with primary key in this list are considered as READ_ONLY (e.g., for default records)
    cfg_choiceLB       = lb_simulation_cfg     # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm        = form_simulation_cfg   # configuration for record form (typically a SupySQLForm_config)

##################################################################################################################################################################
# Dialoge für Table 2: Parameter: Parameter of the simulation program that may be influenced by IVisit      
##################################################################################################################################################################
class lb_parameter_cfg(lb_singlechoice_cfg):    # Listbox zur Auswahl des Datensatzes
    tables = ['parameter']
    cols   = ['parameter.key', 'parameter.name']
    cols_format = ['5d','35s:35']
    cols_sortbutton = ['ID','Parameter']
    title      = 'Choose Parameter'

class form_parameter_cfg(form_cfg):            # Eingabform
    tables                = ['parameter']
    join_on               = None 
    cols                  = ['parameter.key','parameter.name','parameter.comment','parameter.type'      ,'parameter.range','parameter.listidx'   ]   
    cols_type             = ['str'          ,'str'           , 'str'             ,'optionlist'          ,'str'            ,'str'                 ]
    cols_size             = [40              ,40             ,(40,10)            ,40                    ,40               ,10                    ]   
    cols_ref              = [None            ,None           ,None               ,['int','float','text'],None             ,None                  ]
    cols_readonly         = [1               ,0              ,0                  ,0                     ,0                ,0                     ]
    cols_label            = ['ID'            ,'Parameter'    ,'Comment'          ,'Parameter Type'      ,'Parameter range','Parameter List Index']  
    cols_label_pos        = None
    cols_helptext         = ['ID of Parameter (integer)', 'Name of the parameter', 'Comment on the parameter', '(Element) Type of parameter (either integer, float or text)', \
                             '(Element) Parameter range: either [min,max] or [val1,val2,...] or [] if none',\
                             'Parameter Index if only a single value of a parameter list should be controlled (choose -1 if the whole list should be controlled)']
    select_cols           = ['parameter.key']
    select_vals           = [0]                                # default value seems irrelevant here (overwritten by tableditor...)
    update_tables = ['parameter']                                   # tables to be updated after form submission
    update_tables_pkeys = [['parameter.key']]                       # for each table (to be updated) a list of primary keys 
    update_tables_cols  = [['parameter.name','parameter.comment','parameter.type','parameter.range','parameter.listidx']] # for each table (to be updated) a list of columns to be updated
    title      = 'Edit Parameter Instance ...'                    # is used only for askSupySQLForm

class tbed_parameter_cfg(tbed_config):        # Tabellenbearbeitung
    table_cfg          = tb_parameter_cfg     # table to be edited, first column is assumed to be primary key of type INTEGER!!!
    pkeys_readonly     = [] #[0]                   # records with primary key in this list are considered as READ_ONLY (e.g., for default records)
    cfg_choiceLB       = lb_parameter_cfg     # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm        = form_parameter_cfg   # configuration for record form (typically a SupySQLForm_config)

##################################################################################################################################################################
# Dialoge für Table 3: DataArray: DataArray of the simulation program that may be influenced by IVisit      
##################################################################################################################################################################
class lb_dataarray_cfg(lb_singlechoice_cfg):    # Listbox zur Auswahl des Datensatzes
    tables = ['dataarray']
    cols   = ['dataarray.key', 'dataarray.name','dataarray.type']
    cols_format = ['5d','35s:35','20s:20']
    cols_sortbutton = ['ID','Data array','Type']
    title      = 'Choose Data-Array'

class form_dataarray_cfg(form_cfg):            # Eingabform
    tables                = ['dataarray']
    join_on               = None 
    cols                  = ['dataarray.key','dataarray.name','dataarray.comment','dataarray.type'               ,'dataarray.range']   
    cols_type             = ['str'          ,'str'           , 'str'             ,'optionlist'                   ,'str'            ]
    cols_size             = [40              ,40             ,(40,10)            ,40                             ,40               ]   
    cols_ref              = [None            ,None           ,None               ,['int','float','binary','text'],None             ]
    cols_readonly         = [1               ,0              ,0                  ,0                              ,0                ]
    cols_label            = ['ID'            ,'Name of data' ,'Comment'          ,'Data type'                    ,'Data range'     ]  
    cols_label_pos        = None
    cols_helptext         = ['ID of Data array (integer)', 'Name of the data variable in simulation program', 'Comment on the data variable', 'Type of data (either integer, float, binary or text)', \
                             'Data range in form [min,max]; (relevant only for numeric image-type data)']
    select_cols           = ['dataarray.key']
    select_vals           = [0]                                     # default value seems irrelevant here (overwritten by tableditor...)
    update_tables = ['dataarray']                                   # tables to be updated after form submission
    update_tables_pkeys = [['dataarray.key']]                       # for each table (to be updated) a list of primary keys 
    update_tables_cols  = [['dataarray.name','dataarray.comment','dataarray.type','dataarray.range']] # for each table (to be updated) a list of columns to be updated
    title      = 'Edit Data-Array Instance ...'                    # is used only for askSupySQLForm

class tbed_dataarray_cfg(tbed_config):        # Tabellenbearbeitung
    table_cfg          = tb_dataarray_cfg     # table to be edited, first column is assumed to be primary key of type INTEGER!!!
    pkeys_readonly     = [] #[0]                   # records with primary key in this list are considered as READ_ONLY (e.g., for default records)
    cfg_choiceLB       = lb_dataarray_cfg     # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm        = form_dataarray_cfg   # configuration for record form (typically a SupySQLForm_config)

##################################################################################################################################################################
# Dialoge for Table 4: ParameterWidget: Widget class for displaying and modifying parameters    
##################################################################################################################################################################

class lb_parameterwidget_cfg(lb_singlechoice_cfg):
    tables = ['parameterwidget','simulation','parameter']
    join_on = ['parameterwidget.key_simulation=simulation.key', 'parameterwidget.key_parameter=parameter.key']
    cols   = ['parameterwidget.key','parameterwidget.name','simulation.key','simulation.name','simulation.grade','parameter.key','parameter.name']
    cols_format = ['5d','20s:20','5d','20s:20','5d','5d','20s:20']
    cols_sortbutton = ['ID','NAME','ID-SIM','SIM-NAME','SIM-GRADE','ID-PAR','PAR-NAME']
    width = 80
    title      = 'Choose a ParameterWidget'

class form_parameterwidget_cfg(form_cfg):
    tables                = ['parameterwidget']
    join_on               = None
    cols                  = ['parameterwidget.key'    ,'parameterwidget.key_simulation'      ,'parameterwidget.key_parameter','parameterwidget.name'     ,\
                             'parameterwidget.comment','parameterwidget.type'                ,'parameterwidget.range'        ,'parameterwidget.items'    ,\
                             'parameterwidget.size'   ,'parameterwidget.pos'                 ,'parameterwidget.value']
    cols_type             = ['str'                    ,'ref'                                 ,'ref'                          ,'str'                      ,\
                             'textfield'              ,'optionlist'                          ,'str'                          ,'str'                      ,\
                             'str'                    ,'str'                                 ,'str'                  ] 
    cols_ref              = [None                     ,lb_simulation_cfg                     ,lb_parameter_cfg               ,None                       ,\
                             None                     ,['slider','listselection','checkbox','radiobutton','button','textfield'],None                           ,None                       ,\
                             None                     ,None                                  ,None                   ]
    cols_readonly         = [1                        ,0                                     ,0                              ,0                          ,\
                             0                        ,0                                     ,0                              ,0                          ,\
                             0                        ,0                                     ,0                      ]
    cols_label            = ['ID'                     ,'Simulation-ID'                       ,'Parameter-ID'                 ,'Par-Widget-Name'          ,\
                             'Par-Widget-Comment'     ,'Par-Widget-Type'                     ,'Par-Widget-Range'             ,'Par-Widget-Items'         ,\
                             'Par-Widget-Size'        ,'Par-Widget-Position'                 ,'Value'                ] 
    cols_label_pos        = None
    cols_helptext         = ['ID (integer)', 'ID of Simulation Instance', 'ID of Parameter', 'Name of Parameter-Widget', 'Comment on Parameter-Widget', \
                             'Type of Parameter-Widget (either Slider, ListSelection, Checkbox, Radiobutton, Button, or TextField)', \
                             'Range of Parameter-Widget in Format [min, max, nTicks, scale]\n The list fiels nTicks and scale correspond to sliders number of ticks and resolution',\
                             'List of Items for a list selection widget in format [item1,item2,...]', 'Size of Parameter-Widget in Format [sz_x,sz_y]', \
                             'Position of Parameter-Widget in Format [x,y]','Value of Parameter-Widget (as Text)'] 
    #select_cols           = []
    #select_vals           = []                               # default value seems irrelevant here (overwritten by tableditor...)
    select_cols           = ['parameterwidget.key']
    select_vals           = [0]                               # default value seems irrelevant here (overwritten by tableditor...)
    update_tables = ['parameterwidget']                       # tables to be updated after form submission
    update_tables_pkeys = [['parameterwidget.key']]           # for each table (to be updated) a list of primary keys 
    update_tables_cols  = [['parameterwidget.key_simulation','parameterwidget.key_parameter','parameterwidget.name','parameterwidget.comment',\
                            'parameterwidget.type','parameterwidget.range','parameterwidget.items','parameterwidget.size','parameterwidget.pos',\
                            'parameterwidget.value']] # list of columns to be updated
    title      = 'Edit Parameter-Widget...'                   # is used only for askSupySQLForm

class tbed_parameterwidget_cfg(tbed_config):
    table_cfg          = tb_parameterwidget_cfg          # table to be edited, first column is assumed to be primary key of type INTEGER!!!
    pkeys_readonly     = []                              # records with primary key in this list are considered as READ_ONLY (e.g., for default records)
    cfg_choiceLB       = lb_parameterwidget_cfg          # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm        = form_parameterwidget_cfg        # configuration for record form (typically a SupySQLForm_config)
    
##################################################################################################################################################################
# Dialoge for Table 5: DataWidget: Widget class for displaying data        
##################################################################################################################################################################

class lb_datawidget_cfg(lb_singlechoice_cfg):
    tables = ['datawidget','simulation','dataarray']
    join_on = ['datawidget.key_simulation=simulation.key', 'datawidget.key_dataarray=dataarray.key']
    cols   = ['datawidget.key','datawidget.name','simulation.key','simulation.name','dataarray.key','dataarray.name']
    cols_format = ['5d','20s:20','5d','20s:20','5d','20s:20']
    cols_sortbutton = ['ID','NAME','ID-SIM','SIM-NAME','ID-DATA','DATA-NAME']
    width = 80
    title      = 'Choose a Data-Widget'

class form_datawidget_cfg(form_cfg):
    tables                = ['datawidget']
    join_on               = None
    cols                  = ['datawidget.key'  ,'datawidget.key_simulation','datawidget.key_dataarray',                                                              \
                             'datawidget.name' ,'datawidget.comment'       ,'datawidget.type'         ,'datawidget.range' ,'datawidget.pos'      ,'datawidget.scale' ]
    cols_type             = ['str'             ,'ref'                      ,'ref'                     ,                                                              \
                             'str'             ,'textfield'                ,'optionlist'              ,'str'              ,'str'                 ,'str'              ] 
    cols_ref              = [None              ,lb_simulation_cfg          ,lb_dataarray_cfg          ,                                                              \
                             None              ,None                       ,['image','textfield']     ,None               ,None                  ,None               ] 
    cols_readonly         = [1                 ,0                          ,0                         ,                                                              \
                             0                 ,0                          ,0                         ,0                  ,0                     ,0                  ]
    cols_label            = ['ID'              ,'Simulation-ID'            ,'Data-Array-ID'           ,                                                              \
                             'Data-Widget-Name','Data-Widget-Comment'      ,'Data-Widget-Type'        ,'Data-Widget-Range','Data-Widget-Position','Data-Widget-Scale']
    cols_label_pos        = None
    cols_helptext         = ['ID (integer)', 'ID of Simulation Instance', 'ID of Data-Array', 
                             'Name of DataArray-Widget', 'Comment on DataArray-Widget', 'Type of DataArray-Widget (either Image or TextField)', \
                             'Range of DataArray-Widget in Format [min, max] (applies only for image-type data)', 'Position of DataArray-Widget in Format [x,y]', \
                             'Scale used for Dataarray-Widget (applies only for images), e.g., scale=2 means that an image displayed in a widget has double the size of the original image.'+
                             'For Textfields scale<1 means that the widget name is _not_ displayed!']
    select_cols           = ['datawidget.key']
    select_vals           = [0]                               # default value seems irrelevant here (overwritten by tableditor...)
    update_tables = ['datawidget']                       # tables to be updated after form submission
    update_tables_pkeys = [['datawidget.key']]           # for each table (to be updated) a list of primary keys 
    update_tables_cols  = [['datawidget.key_simulation','datawidget.key_dataarray','datawidget.name','datawidget.comment',\
                            'datawidget.type','datawidget.range','datawidget.pos','datawidget.scale']] # list of columns to be updated
    title      = 'Edit Data-Array-Widget...'                      # is used only for askSupySQLForm

class tbed_datawidget_cfg(tbed_config):
    table_cfg          = tb_datawidget_cfg          # table to be edited, first column is assumed to be primary key of type INTEGER!!!
    pkeys_readonly     = []                              # records with primary key in this list are considered as READ_ONLY (e.g., for default records)
    cfg_choiceLB       = lb_datawidget_cfg          # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm        = form_datawidget_cfg        # configuration for record form (typically a SupySQLForm_config)
    

##################################################################################################################################################################
# Dialoge for Table 6: CommentWidget: Widget class for displaying comments        
##################################################################################################################################################################

class lb_commentwidget_cfg(lb_singlechoice_cfg):
    tables = ['commentwidget','simulation']
    join_on = ['commentwidget.key_simulation=simulation.key']
    cols   = ['commentwidget.key','commentwidget.name','simulation.key','simulation.name']
    cols_format = ['5d','20s:20','5d','20s:20']
    cols_sortbutton = ['ID','NAME','ID-SIM','SIM-NAME']
    width = 80
    title      = 'Choose a Comment-Widget'

class form_commentwidget_cfg(form_cfg):
    tables                = ['commentwidget']
    join_on               = None
    cols                  = ['commentwidget.key'     ,'commentwidget.key_simulation','commentwidget.name'     ,'commentwidget.comment','commentwidget.type'           ,'commentwidget.fontname',\
                             'commentwidget.fontsize','commentwidget.fontstyle'     ,'commentwidget.fontcolor','commentwidget.bgcolor','commentwidget.flagDisplayName','commentwidget.pos']
    cols_type             = ['str'                   ,'ref'                         ,'str'                    ,'textfield'            ,'optionlist'                   ,'str'                   ,\
                             'str'                   ,'str'                         ,'str'                    ,'str'                  ,'str'                          ,'str'              ] 
    cols_ref              = [None                    ,lb_simulation_cfg             ,None                     ,None                   ,['textfield']                  ,None                    ,\
                             None                    ,None                          ,None                     ,None                   ,None                           ,None               ] 
    cols_readonly         = [1                       ,0                             ,0                        ,0                      ,0                              ,0                       ,\
                             0                       ,0                             ,0                        ,0                      ,0                              ,0                  ]
    cols_label            = ['ID'                    ,'Simulation-ID'               ,'Widget-Name'            ,'Comment'              ,'Type'                         ,'Font name'             ,\
                             'Font size'             ,'Font style'                  ,'Font color'             ,'Background color'     ,'flagDisplayName'              ,'Widget Position'  ]
    cols_label_pos        = None
    cols_helptext         = ['ID (integer)', 'ID of Simulation Instance', 'Name of Comment-Widget', 'Comment', 'Type of Comment-Widget (either "textfield" or ???)', \
                             'Font name (e.g., Arial)', 'Font size (e.g., 10)', 'Font style (e.g., normal)', 'Font color (e.g., black)','Background color (e.g., gray)', \
                             'Flag indicating whether widget name is displayed (1) or not (0)','Position of DataArray-Widget in Format [x,y]']
    select_cols           = ['commentwidget.key']
    select_vals           = [0]                          # default value seems irrelevant here (overwritten by tableditor...)
    update_tables = ['commentwidget']                       # tables to be updated after form submission
    update_tables_pkeys = [['commentwidget.key']]           # for each table (to be updated) a list of primary keys 
    update_tables_cols  = [['commentwidget.key_simulation','commentwidget.name' ,'commentwidget.comment'       ,'commentwidget.type'         ,\
                            'commentwidget.fontname' ,'commentwidget.fontsize' ,'commentwidget.fontstyle' ,'commentwidget.fontcolor' ,'commentwidget.bgcolor',\
                            'commentwidget.flagDisplayName','commentwidget.pos']] # list of columns to be updated
    title      = 'Edit Comment-Widget...'                      # is used only for askSupySQLForm

class tbed_commentwidget_cfg(tbed_config):
    table_cfg          = tb_commentwidget_cfg          # table to be edited, first column is assumed to be primary key of type INTEGER!!!
    pkeys_readonly     = []                              # records with primary key in this list are considered as READ_ONLY (e.g., for default records)
    cfg_choiceLB       = lb_commentwidget_cfg          # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm        = form_commentwidget_cfg        # configuration for record form (typically a SupySQLForm_config)
    

##################################################################################################################################################################
##################################################################################################################################################################
#        
# Part III: Hub Dialogs (according to expected Workflow)  
#        
##################################################################################################################################################################
##################################################################################################################################################################

##################################################################################################################################################################
# HUB-I Dialog: Erfassung von Simulationen    
##################################################################################################################################################################

#non-simple
class ntom_simulation_parameterwidget_cfg(ntm_nonsimple):    # n-to-m-listbox (!!!!!)
    tables  = ['simulation','parameterwidget','parameter']
    join_on = ['parameterwidget.key_simulation=simulation.key','parameterwidget.key_parameter=parameter.key']
    cols   = ['parameterwidget.key','parameterwidget.name','parameterwidget.type','parameter.name', 'parameterwidget.value']
    cols_format = ['5d','15s:15','10s:10','15s:15','10s:10']
    cols_sortbutton = ['ID','NAME','TYPE','PAR-NAME','VALUE']
    width = 90
    link_ntom_form_cfg=tbed_parameterwidget_cfg
    ntom_copy_cascade = [('simulation','key'), ('parameterwidget','key','key_simulation',['key_parameter','name','comment','type','range','items','size','pos','value'])]  #None    # [(table1,key1),(tablenm,keynm,foreignkey,[list of columns to be copied])]

class ntom_simulation_datawidget_cfg(ntm_nonsimple):    # n-to-m-listbox (!!!!!)
    tables  = ['simulation','datawidget','dataarray']
    join_on = ['datawidget.key_simulation=simulation.key','datawidget.key_dataarray=dataarray.key']
    cols   = ['datawidget.key', 'datawidget.name', 'datawidget.type','dataarray.name', 'dataarray.type']
    cols_format = ['5d','15s:15','10s:10','15s:15','10s:10']
    cols_sortbutton = ['ID','NAME','TYPE','DATA-NAME','DATA-TYPE']
    width = 90
    link_ntom_form_cfg=tbed_datawidget_cfg
    ntom_copy_cascade = [('simulation','key'), ('datawidget','key','key_simulation',['key_dataarray','name','comment','type','range','pos','scale'])]  #None    # [(table1,key1),(tablenm,keynm,foreignkey,[list of columns to be copied])]

class ntom_simulation_commentwidget_cfg(ntm_nonsimple):    # n-to-m-listbox (!!!!!)
    tables  = ['simulation','commentwidget']
    join_on = ['commentwidget.key_simulation=simulation.key']
    cols   = ['commentwidget.key', 'commentwidget.name', 'commentwidget.type']
    cols_format = ['5d','20s:20','20s:20']
    cols_sortbutton = ['ID','NAME','TYPE']
    width = 60
    link_ntom_form_cfg=tbed_commentwidget_cfg
    ntom_copy_cascade = [('simulation','key'), ('commentwidget','key','key_simulation',['name','comment','type','fontname','fontsize','fontstyle','fontcolor','bgcolor','flagDisplayName','pos'])]  # [(table1,key1),(tablenm,keynm,foreignkey,[list of columns to be copied])]

#form...
class formHUB_simulation_cfg(form_cfg):
    tables                = ['simulation']
    join_on               = None 
    cols                  = ['simulation.key'            ,'simulation.name'          ,'simulation.comment','simulation.date_init'             ,'simulation.date_lastmod'     ,'simulation.simsteps_per_frame' ,\
                             'simulation.frames_per_step','simulation.delay_per_step','simulation.grade'  ,None                               ,None                          ,None                             ] 
    cols_type             = ['str'                       ,'str'                      ,'textfield'         ,'str'                              ,'str'                         ,'str'                           ,\
                             'str'                       ,'str'                      ,'str'               ,'ref_ntom'                         ,'ref_ntom'                    ,'ref_ntom'                       ] 
    cols_ref              = [None                        ,None                       ,None                ,None                               ,None                          ,None                            ,\
                             None                        ,None                       ,None                ,ntom_simulation_parameterwidget_cfg,ntom_simulation_datawidget_cfg,ntom_simulation_commentwidget_cfg]
    cols_readonly         = [1                           ,0                          ,0                   ,0                                  ,0                             ,0                               ,\
                             0                           ,0                          ,0                   ,0                                  ,0                             ,0                                ] 
    cols_label            = ['ID'                        ,'Simulation'               ,'Comment'           ,'Date (creation)'                  ,'Date (last mod)'             ,'Simsteps/Frame'                ,\
                             'Frames/Step'               ,'Delay/Step'               ,'Grade'             ,'Parameter-Widgets'                ,'Data-Widgets'                ,'Comment-Widgets'                ] 
    cols_size             = [40                          ,40                         ,(40,7)              ,10                                 ,10                            ,10                              ,\
                             10                          ,10                         ,10                  ,(70,10)                            ,(70,5)                        ,(70,5)]     # may also be list
    cols_helptext         = ['ID of Simulation (integer)'       , 'Name of the simulation'    ,'Comment on the simulation','Date of creation of this simulation file', 'Date of last modification', \
                             'Number of Simulation Steps per Display Frame','Number of Display Frames per IVisit call to step()','Delay [msec] per IVisit call to step()', \
                             'Grade of the simulation, that is, a performance measure of the simulation program with the associated parameter values (choose by hand)', \
                             'Parameter widgets for this simulation', 'Data widgets for this simulation','Comment widgets for this simulation']
    #cols2copy             = ['picture','key_sex','key_religion']   # if None all columns can be copied (e.g., by Tableeditor.on_lb_copy...); otherwise list of columns (of main table!) to be copied
    select_cols           = ['simulation.key']
    select_vals           = [0]                                   # default value seems irrelevant here (overwritten by tableditor...)
    update_tables = ['simulation']                       # tables to be updated after form submission
    update_tables_pkeys = [['simulation.key']]           # for each table (to be updated) a list of primary keys 
    update_tables_cols  = [['simulation.name','simulation.comment','simulation.date_init','simulation.date_lastmod',\
                            'simulation.simsteps_per_frame','simulation.frames_per_step','simulation.delay_per_step','simulation.grade']] # for each table (to be updated) a list of columns to be updated
    title      = 'Edit Simulation and associated parameter, data, and comment widgets...'                      # is used only for askSupySQLForm

#tableeditor...
class tbedHUB_simulation_cfg(tbed_config):
    table_cfg          = tb_simulation_cfg          # table to be edited, first column is assumed to be primary key of type INTEGER!!!
    pkeys_readonly     = [0]                        # records with primary key in this list are considered as READ_ONLY (e.g., for default records)
    cfg_choiceLB       = lb_simulation_cfg          # configuration for choice listbox (typically a SQLListbox_config)
    cfg_recForm        = formHUB_simulation_cfg     # configuration for record form (typically a SupySQLForm_config)








##################################################################################################################################################################
##################################################################################################################################################################
# Module test
##################################################################################################################################################################
##################################################################################################################################################################

if __name__ == '__main__':
    print("\nModule test of ivisit.defdb.py")
    print("------------------------------------\n") 
    db = sqldatabase(db_ivisit_cfg)
    #db.print_database(1)
    r=None 
    res = editSQLTables(r,db,"Edit DB-Table Simulation",tbed_simulation_cfg)
