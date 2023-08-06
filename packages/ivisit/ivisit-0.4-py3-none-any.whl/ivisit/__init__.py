#!/usr/bin/python
# -*- coding: utf-8-unix -*-
    
################################################################################
# IViSiT 0.3: Interactive Visual Simulation Tool
#             based on Python/Tkinter for optimizing model parameters 
# progammed in September 2017 by Andreas Knoblauch
# All rights reserved
#
# Uses the tkinter widgets to implement a generic simulatiom framework
# including input/output widgets for online modifying of simulation parameters
# and online displaying of simulation states
#
# basic simulation framework inspired from neural simulation software PyFelix++
#
################################################################################
     
Version = '0.4'
import sys, os, shutil, traceback                         # platform, args, run tools
import time,datetime
import __main__ as main
#import csv
#import numpy as np
#import matplotlib.dates
#from LevelMacherFrame import *
#import matplotlib.pyplot as plt    
from tkinter        import *               # base widgets, constants
from tkinter.filedialog import Open, SaveAs    # standard dialogs
from tkinter.messagebox import showinfo, showerror, askyesno
#from tkSimpleDialog import askstring, askinteger
#from tkColorChooser import askcolor
from supy.guimaker3 import *               # Frame + menu/toolbar builders
from supy.utilities import *
from ivisit.defdb import *
from ivisit.defdialogs import *
from ivisit.widgetdefcollection import *
from ivisit.widgets import *
from ivisit.parser import *
from ivisit.help import *

#from LevelMacher_databases_oldversion import *   # old versions (just for importing data from old versions)
#from LevelMacher_databases import *
#from LevelMacher_displayframe import *
#from SpielMacher_PythonBuilder import *
#PyLevelMacher_widgetdef import *
#from PyLevelMacher_interface import *
#from PyLevelMacher_widgets import *
#from PyLevelMacher_display import *
#from PyLevelMacher_form import *

try:
    import textConfig                      # startup font and colors
    configs = textConfig.__dict__          # work if not on the path or bad
except:
    configs = {}

helptext = """IVisit Version %s
--------------------
Interactive VIsual SImulation Tool 
for Python-based generic model simulation and optimization of model parameters

(c) 1/9/2017-24/7/2022, Andreas Knoblauch.
All rights reserved.
EXPERIMENTAL SOFTWARE: 
NO WARRANTIES! REGULARLY BACKUP YOUR DATA!

Author:
Andreas Knoblauch
Hochschule Albstadt-Sigmaringen
Albstadt, Germany

New in version %s:
- available as PyPI package (installable with pip install ivisit)
- option to save images from image widgets 
- modfied text_out widgets (can align text)
- synchronous update mode for parameter widgets
- bug fixes 

Version History:
0.1 : 1/9/2017 GenSim
     - Basic functionality
     - Input/Output Widgets
0.2 : 10/11/2019 
     - Automatic Parsing of simulation parameters 
       and output/display widgets
     - binding of events to widgets
     - reorganized code, bug fixes 
     - renaming from "gensim" (generic simulation framework) 
0.3 : 2/4/2021
     - improved image widgets (with context menu)
     - interface to matplotlib 
     - new widgets (checkbox, radiobutton, button)
     - improved help function
     - bug fixes 
0.4 : 24/7/2022
     - available as PyPI package (install with: pip install ivisit)
     - option to save images from image widgets 
     - modfied text_out widgets (can align text)
     - synchronous update mode for parameter widgets
     - bug fixes 
"""

START     = '1.0'                          # index of first char: row=1,col=0
SEL_FIRST = SEL + '.first'                 # map sel tag to index
SEL_LAST  = SEL + '.last'                  # same as 'sel.last'
     
FontScale = 0                              # use bigger font on linux
if sys.platform[:3] != 'win':              # and other non-windows boxes
    FontScale = 3


################################################################################
# Main class: implements IVisit gui, actions
################################################################################

class IVisit:                          # mix with menu/toolbar Frame class
    ftypes = [('All files',     '*'),                       # for file open dialog
              ('IVisit database files',   '.db')]           # customize in subclass
     
    colors = [{'fg':'black',      'bg':'white'},      # color pick list
              {'fg':'yellow',     'bg':'black'},      # first item is default
              {'fg':'white',      'bg':'blue'},       # tailor me as desired
              {'fg':'black',      'bg':'beige'},      # or do PickBg/Fg chooser
              {'fg':'yellow',     'bg':'purple'},
              {'fg':'black',      'bg':'brown'},
              {'fg':'lightgreen', 'bg':'darkgreen'},
              {'fg':'darkblue',   'bg':'orange'},
              {'fg':'orange',     'bg':'darkblue'}]
     
    fonts  = [('courier',    9+FontScale, 'normal'),  # platform-neutral fonts
              ('courier',   12+FontScale, 'normal'),  # (family, size, style)
              ('courier',   10+FontScale, 'bold'),    # or popup a listbox
              ('courier',   10+FontScale, 'italic'),  # make bigger on linux
              ('times',     10+FontScale, 'normal'),  # use 'bold italic' for 2
              ('helvetica', 10+FontScale, 'normal'),  # also 'underline', etc.
              ('ariel',     10+FontScale, 'normal'),
              ('system',    10+FontScale, 'normal'),
              ('courier',   20+FontScale, 'normal')]
     
    def __init__(self, loadFirst='',sim=None,debuglevel=0):
        if not isinstance(self, GuiMaker):
            raise TypeError('IVisit needs a GuiMaker mixin')
        if not isinstance(sim, IVisit_Simulation):
            raise TypeError('Parameter sim must be a IVisit_Simulation')
        self.sim=sim            # reference to simulation class
        self.db=None            # database with widget defintions etc.
        self.debuglevel=debuglevel # debug level (default 0, no debug outputs)
        self.wdefcoll=None          # widget definition
        self.display=None       # display frame
        self.steps=0            # simulation step counter
        self.runflg=0           # if 1 then simulation is running automatically
        self.lastfind   = None
        self.openDialog = None
        self.saveDialog = None
        self.currfile='ivisit_default.db'
         #self.text.focus()                          # else must click in text
        print("loadFirst:",loadFirst)
        if loadFirst: 
            self.onOpen(loadFirst)
        else:
            self.loadDatabase(self.currfile)
            loadFirst=self.currfile
        self.setFileName(loadFirst)
        self.updateTimeLabel()
 
    def start(self):                                # run by GuiMaker.__init__
        self.menuBar = [                            # configure menu/toolbar
            ('File', 0,                    # a GuiMaker menu def tree
                 [('Open...',    0, self.onOpen),   # build in method for self
                  ('Save',       0, self.onSave),   # label, shortcut, callback
                  ('Save As...', 5, self.onSaveAs),
                  ('New',        0, self.onNew),
                  'separator',
                  ('Export',     0, self.onExport),
                  'separator',
                  ('Import Databases'       , 0, self.onImportDatabases),
                  'separator',
                  ('Import From Old Version', 0, self.onImportFromOldVersion),
                  'separator',
                  ('Parse From File', 0, self.onParseFromFile),
                  'separator',
                  ('Quit...',    0, self.onQuit)]
            ),
            ('HUBS', 0,                             
                 [('Simulations'             ,0, self.onHUB_Simulation),
                  'separator',
                  ('Edit Parameter Widgets'  ,0, self.onDB_ParameterWidget),
                  ('Edit Data Widgets'       ,0, self.onDB_DataWidget),
                  'separator',
                  ('Edit Parameters'         ,0, self.onDB_Parameter),
                  ('Edit Data Arrays'        ,0, self.onDB_DataArray)]
            ),
            ('Databases', 0,
                 [('Simulations'                             , 0, self.onDB_Simulation          ),
                  ('Parameters'                              , 0, self.onDB_Parameter           ),
                  ('Data Arrays'                             , 0, self.onDB_DataArray           ),
                  'separator',
                  ('Parameter Widgets'                       , 0, self.onDB_ParameterWidget     ),
                  ('Data Widgets'                            , 0, self.onDB_DataWidget          ),
                  ('Comment Widgets'                         , 0, self.onDB_CommentWidget       )]
            ),
            ('Simulation', 0,
                 [('main_init'                               , 0, self.onSim_main_init          ),
                  'separator',
                  ('init'                                    , 0, self.onSim_init               ),
                  ('step'                                    , 0, self.onSim_step               ),
                  'separator',
                  ('run'                                     , 0, self.onSim_run                ),
                  ('stop'                                    , 0, self.onSim_stop               ),
                  ('cont'                                    , 0, self.onSim_cont               )]
         )]
        self.toolBar = [
            ('Save'             , self.onSave                , {'side': LEFT}),
            ('Init'             , self.onSim_init            , {'side': LEFT}),
            ('Step'             , self.onSim_step            , {'side': LEFT}),
            ('Run'              , self.onSim_run             , {'side': LEFT}),
            ('Stop'             , self.onSim_stop            , {'side': LEFT}),
            ('Cont'             , self.onSim_cont            , {'side': LEFT}),
            ('Simulations'      , self.onHUB_Simulation      , {'side': LEFT}),
            ('Parse'            , self.onParseFromFile       , {'side': LEFT}),
            ('Help'             , self.help                  , {'side': RIGHT}),
            ('Quit'             , self.onQuit                , {'side': RIGHT})]
     
    def makeWidgets(self):                          # run by GuiMaker.__init__
        labelframe = Frame(self)
        name = Label(labelframe, bg='black', fg='white')       # add below menu, above tool
        name.pack(side=LEFT, fill=X)                           # menu/toolbars are packed
        timelabel = Label(labelframe, bg='black', fg='white')  # add below menu, above tool
        timelabel.pack(side=RIGHT, fill=X)                     # menu/toolbars are packed
        pointerlabel = Label(labelframe)
        pointerlabel.pack(side=RIGHT,fill=X)
        labelframe.pack(side=TOP, fill=X)

        # main display (for environment)
        #self.display = IVisitDisplay(self,IVisitDisplay_config,
        #                                  db_level_environments,db_being_instances,db_initial_positions,db_movement_paths,
        #                                  db_images, db_being_types, db_beings,
        #                                  pointerlabel=pointerlabel
        #                                  )
        #self.display.pack(side=LEFT,expand=True,fill=BOTH)
        #self.inputmask_db_beings_instances  = None
        #self.inputmask_db_initial_positions = None
        #self.inputmask_db_movement_paths = None
        #self.display.bind('<being-selected>',self.onBeingSelected)
        #self.display.bind('<being-moved>'   ,self.onBeingMoved   )
        #self.display.bind('<initpos-selected>',self.onInitPosSelected)
        #self.display.bind('<intipos-moved>'   ,self.onInitPosMoved   )
        #self.display.bind('<mvpath-selected>',self.onMvPathSelected)
        #self.display.bind('<mvpath-moved>'   ,self.onMvPathMoved   )

        # assign local variables to object fields...
        self.labelframe = labelframe
        self.filelabel = name
        self.timelabel = timelabel
        self.pointerlabel = pointerlabel
        self.display = None


    ############################################################################
    # Project menu commands
    ############################################################################
     
    def my_askopenfilename(self,initialdir=".", initialfile=None):      # objects remember last result dir/file
        if not self.openDialog:
           self.openDialog = Open(initialdir=initialdir,initialfile=initialfile, 
                                  filetypes=self.ftypes)
        return self.openDialog.show()
     
    def my_asksaveasfilename(self,initialdir=".", initialfile=None, title=None):    # objects remember last result dir/file
        if not self.saveDialog:
           self.saveDialog = SaveAs(initialdir=initialdir,initialfile=initialfile, 
                                    filetypes=self.ftypes, title=title)
        return self.saveDialog.show()
        
    def onOpen(self, loadFirst=''):
        print 
        idir,ifile = self.getInitialDirectoryAndFile(loadFirst)
        doit = (not self.db) or (not self.wdefcoll) or (not self.display) or \
               (not self.display.isModified) or askyesno('IVisit', 'Simulation GUI definition has changed: discard changes?')
        if doit:
            filename = loadFirst or self.my_askopenfilename(initialdir=idir, initialfile=ifile)
            if filename:
                self.loadDatabase(filename)
                self.setFileName(filename)
                self.onSim_main_init()

    def loadDatabase(self,filename,debuglevel=None):              # load new simulation database with a given filename
        # load simulation database (or set to default)
        if(debuglevel==None): debuglevel=self.debuglevel
        self.db = sqldatabase(db_ivisit_cfg, filename, debugLevel=debuglevel)    
        simkeys = self.db.simple_select(['key'],['simulation'])
        self.key_sim_display=simkeys[-1][0]            # default simulation most recent simulation (previous: 'EMPTY' simulation)
        self.updateWidgetDefs()
        self.setFileName(self.db.filename)

    def updateWidgetDefs(self,key_sim=None):    # update widget definitions for a simulation with a given key
        if key_sim==None: key_sim=self.key_sim_display
        try:
            self.wdefcoll=IVisitWidgetDefCollection(self.db,self.sim)
            self.wdefcoll.initFromDatabase(key_sim)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=sys.stdout)         
            print("Warning: Exception e=",e)
        self.updateDisplay()

    def updateDisplay(self,key_sim=None):      # update display according to widget definitions 
        if(self.display): 
            self.display.destroy()
        try:
            self.display = IVisitRawDisplayFrame(self,self.wdefcoll)
            self.display.pack(side=LEFT,expand=True,fill=BOTH)
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=None, file=sys.stdout)         
            print("Warning: Exception e=",e)

    def onSave(self):
        self.onSaveAs(self.currfile)  # may be None
     
    def getInitialDirectoryAndFile(self,forcefile=None):
        if(forcefile==None)or(forcefile==''):
            forcefile=self.getFileName()
        if(forcefile!=None):
            forcefile  = os.path.abspath(forcefile)
            idir,ifile = os.path.split(forcefile)
        else:
            idir,ifile = self.getFileNamePath(), None
        if(idir==None):
            idir=os.path.get_cwd()
        return idir,ifile
     
    def onSaveAs(self, forcefile=None):
        self.display.saveGUIDataToDatabase()             # save GUI changes to old database
        idir,ifile = self.getInitialDirectoryAndFile(forcefile)
        filename = forcefile or self.my_asksaveasfilename(initialdir=idir, initialfile=ifile, title='Save as')
        #if filename != self.currfile:
        #    self.update_filenames_in_databases(self.currfile, filename)
        if filename != self.currfile:  
            if not os.path.exists(filename) or askyesno('IVisit', 'File '+str(filename)+ ' already exists! Do you want to overwrite it?'):
                try:
                    print("copying saved self.currfile=",self.currfile," to filename",filename)
                    shutil.copy2(self.currfile,filename)
                except Exception as e:
                    showerror('IVisit', str(e)+'\nCould not write file ' + filename + '! Keep old file.')
                else:
                    # if all ok do the same procedure as with 'open'
                    self.loadDatabase(filename)
                    self.setFileName(filename)

    def onNew(self, forcefile=None):
        self.display.saveGUIDataToDatabase()             # save GUI changes to old database
        idir,ifile = self.getInitialDirectoryAndFile(forcefile)
        filename = forcefile or self.my_asksaveasfilename(initialdir=idir, initialfile=ifile, title='New')
        if filename:
            if not os.path.exists(filename) or askyesno('IVisit', 'File '+str(filename)+ ' already exists! Do you want to overwrite it?'):
                try:
                    if os.path.exists(filename): os.remove(filename)
                except Exception as e:
                    showerror('IVisit', str(e)+'\nCould not remove file ' + filename + '! Keep file.')
                else:
                    # if all ok do the same procedure as with 'open'
                    self.onOpen(filename)

       
    def onExport(self):
        idir,ifile=self.getInitialDirectoryAndFile()
        ifile=os.path.splitext(ifile)[0]+".py"
        filename=self.my_asksaveasfilename(initialdir=idir, initialfile=ifile)
        if(filename):
            classname       =self.db_level_environments.get_record_entry("Key/Class")
            derivedfromclass=self.db_level_environments.get_record_entry("Derived\nfrom Class")
            build_level_file(filename,classname,derivedfromclass,self.mb_level,None)

    def onImportDatabases(self,list_of_databases = None):
        if list_of_databases == None:
            list_of_databases = ["images.db",
                                 "sounds.db",
                                 "being_types.db",
                                 "being_CHR_collision.db",
                                 "being_CHR_mobility.db",
                                 "being_CHR_character.db",
                                 "being_CHR_question.db",
                                 "being_CHR_ghost.db",
                                 "beings.db"
                                 ]
        idir,ifile=self.getInitialDirectoryAndFile()
        filename=self.my_askopenfilename(initialdir=idir, initialfile=ifile)
        if filename:
            mb1 = Multibase(mb_level_config,filename)
            self.mb_level.import_data_from_multibase(mb1,list_of_databases)

    #def onImportDatabases(self):
    #    idir,ifile=self.getInitialDirectoryAndFile()
    #    filename=self.my_askopenfilename(initialdir=idir, initialfile=ifile)
    #    if filename:
    #        mb1 = Multibase(mb_level_config,filename)
    #        self.importDatabaseFromTo(mb1.get_database("images.db"             ),self.db_images             )
    #        self.importDatabaseFromTo(mb1.get_database("sounds.db"             ),self.db_sounds             )
    #        self.importDatabaseFromTo(mb1.get_database("being_types.db"        ),self.db_being_types        )
    #        self.importDatabaseFromTo(mb1.get_database("being_CHR_collision.db"),self.db_being_CHR_collision)
    #        self.importDatabaseFromTo(mb1.get_database("being_CHR_mobility.db" ),self.db_being_CHR_mobility )
    #        self.importDatabaseFromTo(mb1.get_database("being_CHR_character.db"),self.db_being_CHR_character)
    #        self.importDatabaseFromTo(mb1.get_database("being_CHR_question.db" ),self.db_being_CHR_question )
    #        self.importDatabaseFromTo(mb1.get_database("being_CHR_ghost.db"    ),self.db_being_CHR_ghost    )
    #        self.importDatabaseFromTo(mb1.get_database("beings.db"             ),self.db_beings             )

    #def importDatabaseFromTo(self,db_from, db_to):
    #    keys_from = db_from.get_list_of_keys()
    #    keys_to   = db_to  .get_list_of_keys()
    #    for k in keys_from:
    #        if not (k in keys_to):
    #            r = db_from.get_record(k)
    #            db_to.set_record(*r)

    def onImportFromOldVersion(self,initfile=""):
        if askyesno('Import Level Multibase with old version configuration', 
                    "Choose a filename of an old-version Level file \n"+
                    "according to the multibase configuration given in python file IVisit_databases_oldversion.py.\n"+
                    "Then this old level-file data will be imported to the current level file.\n\n"):
            idir,ifile = self.getInitialDirectoryAndFile(initfile)
            filename_old = self.my_askopenfilename(initialdir=idir, initialfile=ifile)
            if filename_old:
                self.mb_level.cfg.import_leveldata_from_oldversion(self.mb_level,filename_old)
                self.display.synchronize_with_databases()

    def onParseFromFile(self):
        # (i) choose parsing options
        labels           =['Parse file' ,'Simulation name'            ,'Parsing mode'                              ,'Save before parsing?','Select simulation after parsing?']
        parsemode_options=['filename'   ,None                         ,IVisitParser.PARSEMODE_OPTIONS              ,['yes','no']          ,['yes','no']                      ]
        defaults         =[main.__file__,self.wdefcoll.simulation_name,IVisitParser.PARSEMODE_UpdateOldExceptValues,'yes'                 ,'yes'                             ]
        help_event='<Button-3>'
        help_texts=['Choose python simulation file to be parsed\n(default: current python file)',
                    'Name of simulation for which parameters should be parsed\n(default: current simulation; set "" to choose parsed simulation name)',
                    'Choose one of the following parse options:\n'+IVisitParser.parsemode_helptext,
                    'Save all current GUI settings to simulation databases?\n(recommended "yes")',
                    'After parsing, select simulation for which parameters have been parsed?\n(recommended "yes")']
        parseoptions=askSupyForm(labels,defaults,self,"Choose parsing options (press right button for help)...",'e',30,40,options=parsemode_options,help_event=help_event,help_texts=help_texts)
        if parseoptions:
            opt_filename,opt_simname,opt_parsemode,opt_savebefore,opt_selectafter=parseoptions[0],parseoptions[1],parseoptions[2],parseoptions[3],parseoptions[4]
            if opt_savebefore=='yes':     # Save before parsing?
                self.onSave()
            parser = IVisitParser(opt_filename,self.db,opt_parsemode,opt_simname)     
            if opt_selectafter=='yes':    # Select simulation after parsing?
                if opt_simname==self.wdefcoll.simulation_name:   # selected simulation equals current simulation?
                    sim_key=self.key_sim_display                 # then just use current simulation key (prevent using the "wrong" simulation in case of non-unique simulation names!!)
                else:
                    data=self.db.simple_select(['key'],['simulation'],where="name='"+opt_simname+"'")
                    assert len(data)>0, "Simulation name opt_simname="+str(opt_simname)+" cannot be found in database!? Thus, simulation cannot be selected after parsing!!"
                    sim_key=data[0][0]
                self.onHUBSim_SelectSim(None,sim_key)            # select simulation by key

            #idir,ifile = self.getInitialDirectoryAndFile()  # idir is the initial directory
            #ifile = main.__file__                           # name of main python script
            #filename = self.my_askopenfilename(initialdir=idir, initialfile=ifile)
            #if filename:
            #    parser= IVisitParser(filename,self.db) 
        
    def onQuit(self):
        doit = (not self.display is None and not self.display.isModified) \
               or askyesno('IVisit', 'Simulation GUI definition has changed: Quit and discard changes?')    
        if doit:
            self.quit()                 # Frame.quit via GuiMaker

     
    ############################################################################
    # Edit menu commands
    ############################################################################
    def onEditProjectFile(self):
        pass #fillDBInputMask(self,"View and edit database "+db_images_config.fname,db_images,db_images_config)

    def onEditBeingInstances(self):
        self.onDB_BeingInstances()

    def onEditInitialPositions(self):
        self.onDB_InitialPositions()

    def onEditMovementPaths(self):
        self.onDB_MovementPaths()

    def onEditExtraGoals(self):
        self.onDB_ExtraGoals()

    def onEditPlayers(self):
        self.onDB_Players()

    # ----------------

    def onBeingSelected(self,key):
        if self.inputmask_db_beings_instances:
            self.inputmask_db_beings_instances.selectListboxItem(key)

    def onBeingMoved(self,key,pos):
        if self.inputmask_db_beings_instances:
            self.inputmask_db_beings_instances.selectListboxItem(key)

    def onInitPosSelected(self,key):
        if self.inputmask_db_initial_positions:
            self.inputmask_db_initial_positions.selectListboxItem(key)

    def onInitPosMoved(self,key,pos):
        if self.inputmask_db_initial_positions:
            self.inputmask_db_initial_positions.selectListboxItem(key)

    def onMvPathSelected(self,key):
        if self.inputmask_db_movement_paths:
            self.inputmask_db_movement_paths.selectListboxItem(key)

    def onMvPathMoved(self,key,pos):
        if self.inputmask_db_movement_paths:
            self.inputmask_db_movement_paths.selectListboxItem(key)

    ############################################################################
    # Database menu commands
    ############################################################################
    def onDB_images(self):
        fillDBInputMask(self,"View and edit database "+self.db_images.filename,self.db_images,db_images_config,self.mb_level,self.currfile_path)

    def onDB_sounds(self):
        fillDBInputMask(self,"View and edit database "+self.db_sounds.filename,self.db_sounds,db_sounds_config,self.mb_level,self.currfile_path)

    def onDB_CHRCollision(self):
        fillDBInputMask(self,"View and edit database "+self.db_being_CHR_collision.filename,
                        self.db_being_CHR_collision,db_being_CHR_collision_config,self.mb_level,self.currfile_path)

    def onDB_CHRMobility(self):
        fillDBInputMask(self,"View and edit database "+self.db_being_CHR_mobility.filename,
                        self.db_being_CHR_mobility,db_being_CHR_mobility_config,self.mb_level,self.currfile_path)

    def onDB_CHRCharacter(self):
        fillDBInputMask(self,"View and edit database "+self.db_being_CHR_character.filename,
                        self.db_being_CHR_character,db_being_CHR_character_config,self.mb_level,self.currfile_path)

    def onDB_CHRQuestion(self):
        fillDBInputMask(self,"View and edit database "+self.db_being_CHR_question.filename,
                        self.db_being_CHR_question,db_being_CHR_question_config,self.mb_level,self.currfile_path)

    def onDB_CHRGhost(self):
        fillDBInputMask(self,"View and edit database "+self.db_being_CHR_ghost.filename,
                        self.db_being_CHR_ghost,db_being_CHR_ghost_config,self.mb_level,self.currfile_path)

    def onDB_BeingTypes(self):
        fillDBInputMask(self,"View and edit database "+self.db_being_types.filename,self.db_being_types,db_being_types_config,
                        self.mb_level,self.currfile_path)

    def onDB_Beings(self):
        fillBeingsDBInputMask(self,"View and edit database "+self.db_beings.filename,self.db_beings,db_beings_config,
                              self.mb_level,self.currfile_path)

    def onDB_BeingInstances(self):
        top=Toplevel(self)
        top.transient(self)       # make window transient, e.g., minmize with parent etc.
        top.title("View and edit database "+self.db_being_instances.filename) 
        self.inputmask_db_beings_instances=BeingsInstancesDBInputMask(top,self.db_being_instances,db_being_instances_config,
                                                                      self.mb_level,self.currfile_path,
                                                                      self.db_images,self.db_being_types)
        top.wait_window(self.inputmask_db_beings_instances.box)
        self.inputmask_db_beings_instances=None
        top.destroy()

    def onDB_LevelEnvironments(self):
        fillLevelEnvironmentsDBInputMask(self,"View and edit database "+self.db_level_environments.filename,
                                         self.db_level_environments,db_level_environments_config,self.mb_level)

    def onDB_InitialPositions(self):
        top=Toplevel(self)
        top.transient(self)       # make window transient, e.g., minmize with parent etc.
        top.title("View and edit database "+self.db_initial_positions.filename) 
        self.inputmask_db_initial_positions=DBInputMask(top,self.db_initial_positions,db_initial_positions_config,
                                                        self.mb_level,self.currfile_path)
        top.wait_window(self.inputmask_db_initial_positions.box)
        self.inputmask_db_initial_positions=None
        top.destroy()

    def onDB_MovementPaths(self):
        top=Toplevel(self)
        top.transient(self)       # make window transient, e.g., minmize with parent etc.
        top.title("View and edit database "+self.db_movement_paths.filename) 
        self.inputmask_db_movement_paths=DBInputMask(top,self.db_movement_paths,db_movement_paths_config,
                                                     self.mb_level,self.currfile_path)
        top.wait_window(self.inputmask_db_movement_paths.box)
        self.inputmask_db_movement_paths=None
        top.destroy()

    def onDB_ExtraGoals(self):
        fillDBInputMask(self,"View and edit database "+self.db_extra_goals.filename,self.db_extra_goals,db_extra_goals_config,
                        self.mb_level,self.currfile_path)

    def onDB_Players(self):
        fillDBInputMask(self,"View and edit database "+self.db_players.filename,self.db_players,db_players_config,
                        self.mb_level,self.currfile_path)

    ############################################################################
    # Database menu commands
    ############################################################################
    def onDB_Simulation(self):
        editSQLTables(self,self.db,"Editing of Table 'Simulation'",tbed_simulation_cfg)

    def onDB_Parameter(self):
        editSQLTables(self,self.db,"Editing of Table 'Parameter'",tbed_parameter_cfg)

    def onDB_DataArray(self):
        editSQLTables(self,self.db,"Editing of Table 'DataArray'",tbed_dataarray_cfg)

    def onDB_ParameterWidget(self):
        editSQLTables(self,self.db,"Editing of Table 'ParameterWidget'",tbed_parameterwidget_cfg)

    def onDB_DataWidget(self):
        editSQLTables(self,self.db,"Editing of Table 'DataWidget'",tbed_datawidget_cfg)

    def onDB_CommentWidget(self):
        editSQLTables(self,self.db,"Editing of Table 'CommentWidget'",tbed_commentwidget_cfg)

    def onHUB_Simulation(self):
        editSQLTables(self,self.db,"Defining Simulations and their links to Parameters and Data",tbedHUB_simulation_cfg,flagIndepFromParent=1,\
                      extrabuttons=[['Select','listboxleft',self.onHUBSim_SelectSim]])

    def onHUBSim_SelectSim(self,choiceLB,key_sim=None):
        doit = (not self.display.isModified) or askyesno('IVisit', 'Simulation GUI definition has changed: Select simulation and discard changes?')
        if doit:
            #print("choiceLB=",choiceLB)
            #print("selected_data=",choiceLB.selected_data)
            if choiceLB:
                self.key_sim_display=choiceLB.selected_data[0][0]           # simulation key is first entry of data record of listbox
            elif key_sim:
                self.key_sim_display=key_sim
            #print("new key=",self.key_sim_display)
            self.updateWidgetDefs()
            self.updateFileLabel()
            self.updateTimeLabel()

    ############################################################################
    # Simulation menu commands
    ############################################################################
    def onSim_main_init(self):
        self.sim.main_init() 
        self.onSim_init()
        #self.steps=0
        #self.updateTimeLabel()

    def onSim_init(self): 
        self.sim.init()
        self.sim.bind(self,self.display)
        self.steps=0
        self.updateTimeLabel()

    def onSim_step(self):
        if(self.runflg==0):
            self.doOneStepCycle()
        else:
            self.runflg=0

    def onSim_run(self):
        if(self.runflg==0):
            self.onSim_init()
            self.onSim_cont()
        else:
            self.runflg=0

    def onSim_stop(self):                           # stop simulation
        if(self.runflg==1):
            self.runflg=0

    def doOneStepCycle(self):
        for i in range(self.wdefcoll.simulation_frames_per_step):          # loop over number per display frames per step call
            for j in range(self.wdefcoll.simulation_simsteps_per_frame):
                if self.sim.updateMode=='sync': self.wdefcoll.setAllSimulationParameters()
                self.sim.step()
                self.display.resetButtons()   # reset Button variables after each call to step() (where the values may be checked!!)
            self.steps=self.steps+self.wdefcoll.simulation_simsteps_per_frame
            self.wdefcoll.setAllSimulationDataArrays()
            self.display.updateData()   #updateDisplay()
            self.updateTimeLabel()
            #self.steps=self.libSim.PyFeInter_step(self.widgetdefs.felixsteps_per_frame)
            #self.display.updateData()
            #self.setSimTime()
            #if i<(self.widgetdefs.frames_per_step-1):self.update_idletasks()    # force display of each step ...
        
    def onSim_cont(self):                           # continuous simulation (start and stop)
        self.runflg=1-self.runflg;
        self.step_repeater()

    def step_repeater(self):
        if(self.runflg==1):
            self.doOneStepCycle()
            #print("repeater: delay=",self.wdefcoll.simulation_delay_per_step)
            self.after(self.wdefcoll.simulation_delay_per_step, self.step_repeater)
            


    ############################################################################
    # Simulation menu commands
    ############################################################################

    def onFigure(self):                         # draw data etc.
        if(self.data!=None):
            w = Toplevel(self)
            t = matplotlib.dates.date2num([datetime.datetime.strptime(s,"%m/%d/%Y") for s in self.data['date']])
            v = self.data['close']
            cfg = IVisitPlotFrame_config()
            cfg.x=t
            cfg.y=v
            t_disp_min = matplotlib.dates.num2date(t[-1]).date()-datetime.timedelta(days=90)
            t_disp_max = matplotlib.dates.num2date(t[-1]).date()+datetime.timedelta(days=90)
            t_min      = matplotlib.dates.num2date(t[-1]).date()-datetime.timedelta(days=60)
            t_max      = matplotlib.dates.num2date(t[-1]).date()+datetime.timedelta(days=0)
            t_pred_min = matplotlib.dates.num2date(t[-1]).date()-datetime.timedelta(days=60)
            t_pred_max = matplotlib.dates.num2date(t[-1]).date()+datetime.timedelta(days=30)
            cfg.t_disp_min, cfg.t_disp_max = matplotlib.dates.date2num(t_disp_min), matplotlib.dates.date2num(t_disp_max)
            cfg.t_min     , cfg.t_max      = matplotlib.dates.date2num(t_min)     , matplotlib.dates.date2num(t_max)
            cfg.t_pred_min, cfg.t_pred_max = matplotlib.dates.date2num(t_pred_min), matplotlib.dates.date2num(t_pred_max)
            cfg.mv_avg_window=1
            cfg.sampling_interval=1
            cfg.regr_order, regr_type = 1, 'ml'
            cfg.trafo_flag, cfg.trafo_t1, cfg.trafo_t2 = 1, -5,5
            cfg.extremum_domination=10
            f = IVisitPlotFrame(w,cfg).pack(fill=BOTH, expand=1)
            
    def updateFigure(self):
        t = matplotlib.dates.date2num([datetime.datetime.strptime(s,"%m/%d/%Y") for s in self.data['date']])
        v = self.data['close']
        plt.plot_date(t,v,'k-')
        plt.grid()
        plt.show()


    def onRun(self):                            # run simulation
        if(self.runflg==0):
            self.onInit()
            self.onCont()
        else:
            self.runflg=0

    def onStop(self):                           # stop simulation
        if(self.runflg==1):
            self.runflg=0

    def onInit(self):                           # initialize simulation
        self.libSim.PyFeInter_init()
        self.steps=0
        self.setSimTime()

    def onStep(self):                           # do one simulation step
        if(self.runflg==0):
            self.doOneStepCycle()
        else:
            self.runflg=0

    #def doOneStepCycle(self):
    #    for i in range(self.wdefcoll.frames_per_step):              # loop over number per display frames per step call
    #        self.steps=self.libSim.PyFeInter_step(self.widgetdefs.felixsteps_per_frame)
    #        self.display.updateData()
    #        self.setSimTime()
    #        if i<(self.widgetdefs.frames_per_step-1):self.update_idletasks()    # force display of each step ...
        
    #def onCont(self):                           # continuous simulation (start and stop)
    #    self.runflg=1-self.runflg;
    #    self.step_repeater()

    #def step_repeater(self):
    #    if(self.runflg==1):
    #        self.doOneStepCycle()
    #        self.after(self.widgetdefs.delay_per_step, self.step_repeater)
            
    def onControl(self):                           # edit control parameters
        labels=['simulation steps per frame','frames per cycle','delay per cycle [msec]']
        defaults=[str(self.widgetdefs.felixsteps_per_frame), \
                  str(self.widgetdefs.frames_per_step),\
                  str(self.widgetdefs.delay_per_step)]
        r=askPyFeForm(labels,defaults,self,"Edit simulation control parameters",'w',labelwidth=None,entrysize=20)
        if r:
            self.widgetdefs.felixsteps_per_frame = int(r[0])
            self.widgetdefs.frames_per_step      = int(r[1])
            self.widgetdefs.delay_per_step       = int(r[2])

    def onReparse(self):                           # reparse Felix simulation parameters
        self.runflg=1-self.runflg;
        self.step_repeater()

    def onUndo(self):                           # 2.0
        try:                                    # tk8.4 keeps undo/redo stacks
            pass #self.text.edit_undo()               # exception if stacks empty
        except TclError:                        # menu tear-offs for quick undo
            showinfo('PyEdit', 'Nothing to undo')
            
    def onRedo(self):                           # 2.0: redo an undone
        try:
            pass #self.text.edit_redo()
        except TclError:
            showinfo('PyEdit', 'Nothing to redo')
        
    def onCopy(self):                           # get text selected by mouse,etc
        #if not self.text.tag_ranges(SEL):       # save in cross-app clipboard
        #    showerror('PyEdit', 'No text selected')
        #else:
        #    text = self.text.get(SEL_FIRST, SEL_LAST)  
        #    self.clipboard_clear()              
        #    self.clipboard_append(text)
        pass
    
    def onDelete(self):                         # delete selected text, no save
        pass
        #if not self.text.tag_ranges(SEL):
        #    showerror('PyEdit', 'No text selected')
        #else:
        #    self.text.delete(SEL_FIRST, SEL_LAST)
     
    def onCut(self):
        pass
        #if not self.text.tag_ranges(SEL):
        #    showerror('PyEdit', 'No text selected')
        #else: 
        #    self.onCopy()                       # save and delete selected text
        #    self.onDelete()
     
    def onPaste(self):
        pass
        #try:
        #    text = self.selection_get(selection='CLIPBOARD')
        #except TclError:
        #    showerror('PyEdit', 'Nothing to paste')
        #    return
        #self.text.insert(INSERT, text)          # add at current insert cursor
        #self.text.tag_remove(SEL, '1.0', END) 
        #self.text.tag_add(SEL, INSERT+'-%dc' % len(text), INSERT)
        #self.text.see(INSERT)                   # select it, so it can be cut
     
    def onSelectAll(self):
        pass
        #self.text.tag_add(SEL, '1.0', END+'-1c')   # select entire text 
        #self.text.mark_set(INSERT, '1.0')          # move insert point to top
        #self.text.see(INSERT)                      # scroll to top

    ############################################################################
    # Search menu commands
    ############################################################################
 
    def onGoto(self, forceline=None):
        pass
        #line = forceline or askinteger('PyEdit', 'Enter line number')
        #self.text.update() 
        #self.text.focus()
        #if line is not None:
        #    maxindex = self.text.index(END+'-1c')
        #    maxline  = int(maxindex.split('.')[0])
        #    if line > 0 and line <= maxline:
        #        self.text.mark_set(INSERT, '%d.0' % line)      # goto line
        #        self.text.tag_remove(SEL, '1.0', END)          # delete selects
        #        self.text.tag_add(SEL, INSERT, 'insert + 1l')  # select line
        #        self.text.see(INSERT)                          # scroll to line
        #    else:
        #        showerror('PyEdit', 'Bad line number')
     
    def onFind(self, lastkey=None):
        pass
        #key = lastkey or askstring('PyEdit', 'Enter search string')
        #self.text.update()
        #self.text.focus()
        #self.lastfind = key
        #if key:                                                    # 2.0: nocase
        #    nocase = configs.get('caseinsens', 1)                  # 2.0: config
        #    where = self.text.search(key, INSERT, END, nocase=nocase)
        #    if not where:                                          # don't wrap
        #        showerror('PyEdit', 'String not found')
        #    else:
        #        pastkey = where + '+%dc' % len(key)           # index past key
        #        self.text.tag_remove(SEL, '1.0', END)         # remove any sel
        #        self.text.tag_add(SEL, where, pastkey)        # select key 
        #        self.text.mark_set(INSERT, pastkey)           # for next find
        #        self.text.see(where)                          # scroll display
     
    def onRefind(self):
        pass
        #self.onFind(self.lastfind)
     
    def onChange(self):
        pass
        #new = Toplevel(self)
        #Label(new, text='Find text:').grid(row=0, column=0)
        #Label(new, text='Change to:').grid(row=1, column=0)
        #self.change1 = Entry(new)
        #self.change2 = Entry(new)
        #self.change1.grid(row=0, column=1, sticky=EW)
        #self.change2.grid(row=1, column=1, sticky=EW)
        #Button(new, text='Find',  
        #       command=self.onDoFind).grid(row=0, column=2, sticky=EW)
        #Button(new, text='Apply', 
        #       command=self.onDoChange).grid(row=1, column=2, sticky=EW)
        #new.columnconfigure(1, weight=1)    # expandable entrys
     
    def onDoFind(self):
        pass
        #self.onFind(self.change1.get())                    # Find in change box
     
    def onDoChange(self):
        pass
        #if self.text.tag_ranges(SEL):                      # must find first
        #    self.text.delete(SEL_FIRST, SEL_LAST)          # Apply in change
        #    self.text.insert(INSERT, self.change2.get())   # deletes if empty
        #    self.text.see(INSERT)
        #    self.onFind(self.change1.get())                # goto next appear
        #    self.text.update()                             # force refresh
     
    ############################################################################
    # Tools menu commands 
    ############################################################################
     
    def onFontList(self):
        pass
        #self.fonts.append(self.fonts[0])           # pick next font in list
        #del self.fonts[0]                          # resizes the text area
        #self.text.config(font=self.fonts[0]) 
     
    def onColorList(self):
        pass
        #self.colors.append(self.colors[0])         # pick next color in list
        #del self.colors[0]                         # move current to end
        #self.text.config(fg=self.colors[0]['fg'], bg=self.colors[0]['bg']) 
     
    def onPickFg(self):
        pass
        #self.pickColor('fg')                       # added on 10/02/00
    def onPickBg(self):                             # select arbitrary color
        pass
        #self.pickColor('bg')                       # in standard color dialog

    def pickColor(self, part):                      # this is too easy
        pass
        #(triple, hexstr) = askcolor()
        #if hexstr:
        #    self.text.config(**{part: hexstr})
     
    def onInfo(self):
        pass
        #text  = self.getAllText()                  # added on 5/3/00 in 15 mins
        #bytes = len(text)                          # words uses a simple guess: 
        #lines = len(text.split('\n'))              # any separated by whitespace
        #words = len(text.split()) 
        #index = self.text.index(INSERT)
        #where = tuple(index.split('.'))
        #showinfo('PyEdit Information',
        #         'Current location:\n\n' +
        #         'line:\t%s\ncolumn:\t%s\n\n' % where +
        #         'File text statistics:\n\n' +
        #         'bytes:\t%d\nlines:\t%d\nwords:\t%d\n' % (bytes, lines, words))
     
    def onClone(self):
        new = Toplevel()                # a new edit window in same process
        myclass = self.__class__        # instance's (lowest) class object
        myclass(new)                    # attach/run instance of my class
     
    def onRunCode(self, parallelmode=True):
        """
        run Python code being edited--not an ide, but handy;
        tries to run in file's dir, not cwd (may be PP3E root);
        inputs and adds command-line arguments for script files;
        code's stdin/out/err = editor's start window, if any:
        run with a console window to see code's print outputs;
        but parallelmode uses start to open a dos box for i/o;
        module search path will include '.' dir where started;
        in non-file mode, code's Tk root window is PyEdit win;
        """
        def askcmdargs():
            return askstring('PyEdit', 'Commandline arguments?') or ''
        
        from PP3E.launchmodes import System, Start, Fork
        filemode = False
        thefile  = str(self.getFileName())
        if os.path.exists(thefile):
            filemode = askyesno('PyEdit', 'Run from file?')
        if not filemode:                                    # run text string
            cmdargs   = askcmdargs()
            namespace = {'__name__': '__main__'}            # run as top-level
            sys.argv  = [thefile] + cmdargs.split()         # could use threads
            exec(self.getAllText() + '\n' in namespace)     # exceptions ignored
        elif self.spielmacher_edit_modified:                     # 2.0: changed test
            showerror('PyEdit', 'Text changed: save before run')
        else:
            cmdargs  = askcmdargs()
            mycwd    = os.getcwd()                          # cwd may be root
            os.chdir(os.path.dirname(thefile) or mycwd)     # cd for filenames
            thecmd   = thefile + ' ' + cmdargs
            if not parallelmode:                            # run as file
                System(thecmd, thecmd)()                    # block editor
            else:
                if sys.platform[:3] == 'win':               # spawn in parallel
                    Start(thecmd, thecmd)()                 # or use os.spawnv
                else:
                    Fork(thecmd, thecmd)()                  # spawn in parallel
            os.chdir(mycwd)

    def onPickFont(self):
        pass
        # 2.0 font spec dialog
        #new = Toplevel(self)
        #Label(new, text='Family:').grid(row=0, column=0)      # nonmodal dialog
        #Label(new, text='Size:  ').grid(row=1, column=0)      # see pick list 
        #Label(new, text='Style: ').grid(row=2, column=0)      # for valid inputs
        #self.font1 = Entry(new)
        #self.font2 = Entry(new)
        #self.font3 = Entry(new)
        #self.font1.insert(0, 'courier')                       # suggested vals
        #self.font2.insert(0, '12')
        #self.font3.insert(0, 'bold italic')
        #self.font1.grid(row=0, column=1, sticky=EW)
        #self.font2.grid(row=1, column=1, sticky=EW)
        #self.font3.grid(row=2, column=1, sticky=EW)
        #Button(new, text='Apply', 
        #       command=self.onDoFont).grid(row=3, columnspan=2)
        #new.columnconfigure(1, weight=1)    # expandable entrys

    def onDoFont(self):
        pass
        #try:
        #    font = (self.font1.get(), int(self.font2.get()), self.font3.get())
        #    self.text.config(font=font) 
        #except:
        #    showerror('PyEdit', 'Bad font specification')
     
    ############################################################################
    # Utilities, useful outside this class
    ############################################################################
     
    #def isEmpty(self):
    #    return not self.getAllText() 
     
    #def getAllText(self):
    #    return self.text.get('1.0', END+'-1c')  # extract text as a string     
    #def setAllText(self, text):
    #    self.text.delete('1.0', END)            # store text string in widget
    #    self.text.insert(END, text)             # or '1.0'
    #    self.text.mark_set(INSERT, '1.0')       # move insert point to top 
    #    self.text.see(INSERT)                   # scroll to top, insert set
    #def clearAllText(self):
    #    self.text.delete('1.0', END)            # clear text in widget 
     
    def getFileName(self):                       # full file name
        return self.currfile
    def getFileNameFile(self):                   # only file name without path
        return self.currfile_file
    def getFileNamePath(self):                   # only path
        return self.currfile_path
    def setFileName(self, name):                 # also: onGoto(linenum)
        self.currfile = name  # for save
        if(self.currfile!=None)and(self.currfile!=""):
            self.currfile = os.path.abspath(self.currfile)
            self.currfile_path, self.currfile_file = os.path.split(self.currfile)
        else:
            self.currfile_path, self.currfile_file = "", None
        self.updateFileLabel()
       
    def updateFileLabel(self):
        if(self.currfile==None) or (self.currfile==""):
            self.filelabel.configure(text='None')
        else:
            self.filelabel.configure(text=self.currfile+"::"+str(self.key_sim_display)+"::"+self.wdefcoll.simulation_name)
        
    def updateTimeLabel(self):
        if(self.steps==None) or (self.steps==""):
            self.timelabel.configure(text='None')
        else:
            self.timelabel.configure(text="steps="+str(self.steps))
        

    #def setBg(self, color):
    #    self.text.config(bg=color)              # to set manually from code
    #def setFg(self, color):
    #    self.text.config(fg=color)              # 'black', hexstring
    #def setFont(self, font):
    #    self.text.config(font=font)             # ('family', size, 'style')
        
    #def setHeight(self, lines):                 # default = 24h x 80w
    #    self.text.config(height=lines)          # may also be from textCongif.py
    #def setWidth(self, chars):
    #    self.text.config(width=chars)

    #def clearModified(self):
    #    self.text.edit_modified(0)              # clear modified flag
    def isModified(self):
        return self.spielmacher_edit_modified    # changed since last reset?
 
    def help(self):
        #showinfo('About IVisit', helptext % ((Version,)*2))
        askSupyTextForm(default_text=helptext % ((Version,)*2)+"\n\n"+readme_text,parent=self,title="About IVisit",readonly=True,height=40,width=80, wrap=None)
     
################################################################################
# ready-to-use editor classes 
# mix in a Frame subclass that builds menu/toolbars
################################################################################

#    
# when IVisit owns the window 
#
class IVisitMain(IVisit, GuiMakerWindowMenu):  # add menu/toolbar maker 
    def __init__(self, parent=None, loadFirst='', sim=None, debuglevel=0):     # when fills whole window
        GuiMaker.__init__(self, parent)                 # use main window menus
        IVisit.__init__(self, loadFirst,sim,debuglevel) # self has GuiMaker frame
        self.master.title('IVisit ' + Version)          # title if stand-alone
        self.master.iconname('IVisit')                  # catch wm delete button
        self.master.protocol('WM_DELETE_WINDOW', self.onQuit)
     
class IVisitMainPopup(IVisit, GuiMakerWindowMenu):
    def __init__(self, parent=None, loadFirst='', sim=None, winTitle='', debuglevel=0):     
        self.popup = Toplevel(parent)                  # create own window
        GuiMaker.__init__(self, self.popup)            # use main window menus
        IVisit.__init__(self, loadFirst,sim,debuglevel) 
        assert self.master == self.popup
        self.popup.title('IVisit ' + Version + winTitle) 
        self.popup.iconname('IVisit')               
    def quit(self):
        self.popup.destroy()                           # kill this window only

#         
# when embedded in another window
#
class IVisitComponent(IVisit, GuiMakerFrameMenu):     
    def __init__(self, parent=None, loadFirst='', sim=None, debuglevel=0):     # use Frame-based menus
        GuiMaker.__init__(self, parent)                # all menus, buttons on
        IVisit.__init__(self, loadFirst,sim,debuglevel)           # GuiMaker must init 1st
     
class IVisitComponentMinimal(IVisit, GuiMakerFrameMenu): 
    def __init__(self, parent=None, loadFirst='', sim=None, deleteFile=1, debuglevel=0):   
        self.deleteFile = deleteFile
        GuiMaker.__init__(self, parent)             
        IVisit.__init__(self, loadFirst,sim,debuglevel) 
    def start(self):
        IVisit.start(self)                         # GuiMaker start call
        for i in range(len(self.toolBar)):             # delete quit in toolbar
            if self.toolBar[i][0] == 'Quit':           # delete file menu items
                del self.toolBar[i]; break             # or just disable file
        if self.deleteFile:
            for i in range(len(self.menuBar)):
                if self.menuBar[i][0] == 'File':
                    del self.menuBar[i]; break
        else:
            for (name, key, items) in self.menuBar:
                if name == 'File':
                    items.append([1,2,3,4,6]) 

################################################################################
# stand-alone program run
################################################################################
                                                     
def testPopup():     
    # see PyView and PyMail for component tests
    root = Tk()
    IVisitMainPopup(root)
    IVisitMainPopup(root)
    Button(root, text='More', command=IVisitMainPopup).pack(fill=X)
    Button(root, text='Quit', command=root.quit).pack(fill=X)
    root.mainloop()
     
def IVisit_main(fname=None,sim=None,debuglevel=0):  # may be typed or clicked
    try:                                              # or associated on Windows
        if(fname==None): fname = sys.argv[1]          # arg = optional filename
    except IndexError:
        fname = None
    print("starting with fname=",fname)
    if sim==None: sim=IVisit_Simulation()
    IVisitMain(loadFirst=fname,sim=sim,debuglevel=debuglevel).pack(expand=YES, fill=BOTH)
    mainloop()
     
if __name__ == '__main__':                            # when run as a script
    #testPopup()
    IVisit_main()                                     # run .pyw for no dos box    
