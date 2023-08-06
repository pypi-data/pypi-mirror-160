import os.path
from datetime import datetime
from ivisit.defdb import *
from supy.sqldatabase import *
from supy.utilities import *

# ***************************************************************************
# class IVisitParser:
# Parsing of simulation parameters and data to be displayed  
#    - provides all information necessary 
#      to a create a real widget that can be displayed on the working frame 
#    - A ParameterWidgetDef thereby links a Database ParameterWidget entry 
#      to the corresponding simulation parameters of the simulation program
# ***************************************************************************
class IVisitParser:
    PARSEMODE_OnlyNewWidgets       ='Parse ONLY NEW WIDGETS'
    PARSEMODE_UpdateOld            ='Also UPDATE OLD WIDGETS'
    PARSEMODE_UpdateOldExceptValues='Also UPDATE OLD WIDGETS except VALUES'
    PARSEMODE_OPTIONS=[PARSEMODE_OnlyNewWidgets,PARSEMODE_UpdateOld,PARSEMODE_UpdateOldExceptValues]
    parsemode_helptext= 'Parse ONLY NEW WIDGETS: Keep all existing widgets unmodified\n'+\
                        'Also UPDATE OLD WIDGETS: Overwrite all existing widgets with parsed information\n'+\
                        'Also UPDATE OLD WIDGETS except VALUES: Overwrite all existing widgets with parsed information, but keep widget values\n'

    def __init__(self,filepath,db=None,parsemode=PARSEMODE_UpdateOldExceptValues,sim_name=None):
        self.db=db                # reference to sqldatabase
        self.parsemode=parsemode  # parsing mode
        self.sim_name=sim_name    # simulation name for which parameters should be parsed
        self.parse_lines_of_simulations(filepath)
        #print(self.lines_of_simulations)
        #print(self.linenumbers_of_simulations)
        self.nSimulations = len(self.linenumbers_of_simulations)
        self.tb_simulation_entries=self.nSimulations*[[]]
        self.tb_parameter_entries=self.nSimulations*[[]]
        self.tb_dataarray_entries=self.nSimulations*[[]]
        self.tb_parameterwidget_entries=self.nSimulations*[[]]
        self.tb_datawidget_entries=self.nSimulations*[[]]
        self.tb_commentwidget_entries=self.nSimulations*[[]]
        self.i_sim=0   # initialize simulation index (will be updated by new_simulation...)
        for i in range(self.nSimulations):
            self.parse_simulation(self.lines_of_simulations[i],self.linenumbers_of_simulations[i])

    def parse_lines_of_simulations(self,filepath):
        lines_of_simulations = []               # list of all lists of lines_of_simulations ...
        linenumbers_of_simulations = []         # ... corresponding lists of line numbers
        lines_of_simulation = []                # list of all all text lines that correspond to the current simulation and ...
        linenumbers_of_simulation = []          # ... corresponding list of line numbers (referring to the filepath file) 
        if os.path.isfile(filepath):
            with open(filepath,'r') as f:
                linenumber=0  # initialize line number
                n_simu=0      # initialize number of simulations to be parsed
                for line in f:
                    linenumber=linenumber+1          # number of the line that is currently parsed
                    l=line.strip()                   # remove white space from left and right of line
                    i_ivisit = l.find(r"@IVISIT:")   # index of beginning of @IVISIT definition (or <0)
                    if i_ivisit>=0:                  # is there a @IVISIT definition?
                        assert len(l)>(i_ivisit+8),"IVisitParser Syntax Error in File "+str(filepath)+", line "+str(linenumber)\
                            +": @IVISIT: directive must be followed by some keyword (e.g., SIMULATION, SLIDER, LISTSEL, CHECKBOX, RADIOBUTTON, TEXT_IN, IMAGE, TEXT_OUT)"
                        l=l[(i_ivisit+8):]           # if so, then take rest of line
                        i_comments = l.find(r"#")    # index of beginning of a comment (to be skipped)
                        if i_comments>=0: l=l[0:i_comments]  # skip behind the comment '#'
                        l=l.strip()                  # remove again white space from left and right of line
                        if l.find(r"SIMULATION")==0: # beginning of a new simulation definition?
                            # yes, new simulation definition
                            if len(lines_of_simulation)>0:  # add current line to list of lines and ...
                                lines_of_simulations      .append(lines_of_simulation)
                                linenumbers_of_simulations.append(number_of_lines_of_simulation)
                            lines_of_simulation       = [] # ... reset lists
                            linenumbers_of_simulation = [] # ... ditto
                            n_simu                    = n_simu+1
                        # another line belonging to the current simulation definition
                        assert n_simu>0, "IVisitParser Syntax Error in File "+str(filepath)+", line "+str(linenumber)\
                            +": First @IVISIT definition must begin with @IVISIT:SIMULATION <Name>"
                        lines_of_simulation      .append(l)
                        linenumbers_of_simulation.append(linenumber)
                if len(lines_of_simulation)>0:
                    lines_of_simulations      .append(lines_of_simulation)
                    linenumbers_of_simulations.append(linenumbers_of_simulation)
        self.lines_of_simulations       = lines_of_simulations
        self.linenumbers_of_simulations = linenumbers_of_simulations
        self.filepath=filepath

    def parse_simulation(self,lines_of_simulation, linenumbers_of_simulation):
        assert len(lines_of_simulation)==len(linenumbers_of_simulation),"IVisitParser::parse_simulation(lines_of_simulation,linenumbers_of_simulation): "\
            +"Two parameters must be lists of same length, but len(los)="+str(len(lines_of_simulation))+", len(lnos)="+str(len(linenumbers_of_simulation))+" !"
        for i in range(len(lines_of_simulation)):
            l,ln=lines_of_simulation[i].strip(), str(linenumbers_of_simulation[i])    # get next line
            terms=l.split('&')
            terms=[t.strip() for t in terms]
            nterms = len(terms)
            str_parseerror = "IVisitParser::parse_simulation(.): Parse error in line "+ln+" of file "+self.filepath+": "
            assert nterms>=1, str_parseerror\
                +"Expected key word (either SIMULATION, SLIDER, LISTSEL, TEXT_IN, IMAGE, or TEXT_OUT), but got nothing: terms="+str(terms)
            if terms[0]=="SIMULATION":
                assert i==0, str_parseerror+"SIMULATION DIRECTIVE must occur only once per simulation! But here SIMULATION directive occured i="+str(i)+" times!"
                assert nterms==2, str_parseerror+"Syntax Error in SIMULATION DIRECTIVE, nterms="+str(nterms)+"! Instead please use syntax @IVISIT:SIMULATION § <simulation_name>"
                self.new_simulation(terms[1])
            elif terms[0]=="SLIDER":
                assert nterms==8, str_parseerror+"Syntax Error in SLIDER DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:SLIDER & <slidername> & <size> & <range> & <parametername> & <listindex> & <type> & <value>"
                self.new_slider(terms[1],terms[2],terms[3],terms[4],terms[5],terms[6],terms[7])
            elif terms[0]=="LISTSEL":
                assert nterms==8, str_parseerror+"Syntax Error in LISTSEL DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:LISTSEL & <listsel_name> & <size> & <list_of_options> & <parametername> & <listindex> & <type> & <value>"
                self.new_listsel(terms[1],terms[2],terms[3],terms[4],terms[5],terms[6],terms[7])
            elif terms[0]=="CHECKBOX":
                assert nterms==5, str_parseerror+"Syntax Error in CHECKBOX DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:CHECKBOX & <checkbox_name> & <list_of_options> & <parametername> & <value>"
                self.new_checkbox(terms[1],terms[2],terms[3],terms[4])
            elif terms[0]=="RADIOBUTTON":
                assert nterms==5, str_parseerror+"Syntax Error in RADIOBUTTON DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:RADIOBUTTON & <radiobutton_name> & <list_of_options> & <parametername> & <value>"
                self.new_radiobutton(terms[1],terms[2],terms[3],terms[4])
            elif terms[0]=="BUTTON":
                assert nterms==4, str_parseerror+"Syntax Error in BUTTON DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:BUTTON & <button_name> & [<label_text>,<button_text>] & <parametername>"
                self.new_button(terms[1],terms[2],terms[3])
            elif terms[0]=="TEXT_IN":
                assert nterms==6, str_parseerror+"Syntax Error in TEXT_IN DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:TEXT_IN & <textinbox_name> & <size> & <parametername> & <listindex> & <value>"
                self.new_textin(terms[1],terms[2],terms[3],terms[4],terms[5])
            elif terms[0]=="IMAGE":
                assert nterms==6, str_parseerror+"Syntax Error in IMAGE DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:IMAGE & <image_name> & <scale> & <range> & <dataname> & <type>"
                self.new_image(terms[1],terms[2],terms[3],terms[4],terms[5])
            elif terms[0]=="TEXT_OUT":
                assert nterms==5, str_parseerror+"Syntax Error in TEXT_OUT DIRECTIVE, nterms="+str(nterms)+"! "\
                    +"Instead please use syntax @IVISIT:TEXT_OUT & <textoutbox_name> & <size> & <list_of_options> & <dataname>"
                self.new_textout(terms[1],terms[2],terms[3],terms[4])
            else:
                assert 0, "IVisitParser::parse_simulation(.): After @IVISIT: I expected a key word (either SIMULATION, SLIDER, LISTSEL, TEXT_IN, IMAGE, or TEXT_OUT)"\
                    +"at beginning of line "+ln+" in file "+self.filepath+" ! Instead read terms[0]="+terms[0]+"! Note that terms must be separated by '&'!"

    def new_simulation(self,sim_name):
        if not str(self.sim_name).strip() in ['None','NONE','']:   # replace parsed sim_name (given here by sim_name) by constructor sim_name (given here by self.sim_name) ?
            sim_name=self.sim_name
        #print("new_simulation: sim_name=",sim_name)
        now=datetime.now()
        today_str=now. strftime("%Y.%m.%d")
        #print("today_str=",today_str)
        self.simkey=None        # simulation key to be used for following inserts/updates
        if self.db!=None:
            data=self.db.simple_select(['key'],['simulation'],where="name='"+sim_name+"'")
            #print("data=",data)
            if len(data)<=0:    # no simulation with this name --> insert new simulation record in table
                self.simkey=self.db.get_new_primary_key('simulation')[0]
                #print("new key:=",self.simkey)
                self.db.simple_insert('simulation',['key','name','date_init','date_lastmod'],[self.simkey,sim_name,today_str,today_str])   # insert new simulation entry
            else:              # there is already a simulation with this name --> take first, update table
                self.simkey=data[0][0]
                self.db.simple_update_byPKEY('simulation',['date_lastmod'],[today_str],['key'],[self.simkey])
        
    def new_slider(self,sld_name,sld_size,sld_range,sld_parametername,sld_listidx,sld_type,sld_value):
        #print("new_slider: terms=",sld_name,sld_size,sld_range,sld_parametername,sld_listidx,sld_type,sld_value)
        # (i) prepare parameters
        if sld_type in ['int','INT','integer','INTEGER']: sld_type='int'
        if sld_type in ['float','double','FLOAT','DOUBLE']: sld_type='float'
        range_list=parseStringAsList(sld_range,sld_type,[0,100,5,1])
        par_range=str([0,100])
        if len(range_list)>=2: par_range=str(range_list[0:2])
        parwdg_range=str([0,100,5,1])
        if len(range_list)>=4: parwdg_range=str([range_list[0],range_list[1],int(round(range_list[2])),range_list[3]])  # format [min,max,nticks,scale]
        if self.db!=None:
            # (ii) Create/Modify parameter entry in table 'parameter'
            parkey=None                            # find parameter key
            data=self.db.simple_select(['key'],['parameter'],where="name='"+sld_parametername+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                parkey = self.db.get_new_primary_key('parameter')[0]
                self.db.simple_insert('parameter',['key','name','type','range','listidx'],[parkey,sld_parametername,sld_type,par_range,asNumber(sld_listidx,'int',0)]) # insert new parameter entry
            else:                                                                                                                                      # update parameter entry (depending on mode)
                parkey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameter',['type','range','listidx'],[sld_type,par_range,asNumber(sld_listidx,'int',0)],['key'],[parkey])   # update all available fields 
            # (iii) Create/Modify parameter widget entry in table 'parameterwidget'
            parwdg_key=None                        # find parameter key
            whereclause=self.db.getWhereClause_from_ColumnValues(['parameterwidget'],['key_simulation','key_parameter','name'],[self.simkey,parkey,sld_name])
            data=self.db.simple_select(['key'],['parameterwidget'],where=whereclause)
            if len(data)<=0: # no parameter widget available --> insert new one in table 
                parwdg_key = self.db.get_new_primary_key('parameterwidget')[0]
                self.db.simple_insert('parameterwidget',\
                                      ['key'     ,'key_simulation','key_parameter','name'  ,'type'  ,'range'     ,'size'  ,'value'  ],\
                                      [parwdg_key,self.simkey     ,parkey         ,sld_name,'slider',parwdg_range,sld_size,sld_value])          # insert new parameter entry
            else:                                                                                                                               # update parameter widget entry (depending on mode)
                parwdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type', 'range'      ,'size'  ,'value'],\
                                                 ['slider',parwdg_range,sld_size,sld_value], ['key'],[parwdg_key])                              # update all available fields 
                elif self.parsemode in [self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type', 'range'      ,'size'],\
                                                 ['slider',parwdg_range,sld_size], ['key'],[parwdg_key])                                        # update all available fields except value

    def new_listsel(self,ls_name,ls_size,ls_options,ls_parametername,ls_listidx,ls_type,ls_value):
        #print("new_listsel: terms=",ls_name,ls_size,ls_options,ls_parametername,ls_listidx,ls_type,ls_value)
        # (i) prepare parameters
        if ls_type in ['string','STRING','text','TEXT']: ls_type='text'
        if ls_type in ['int','INT','integer','INTEGER']: ls_type='int'
        if ls_type in ['float','FLOAT','double','DOUBLE']: ls_type='float'
        if self.db!=None:
            # (ii) Create/Modify parameter entry in table 'parameter'
            parkey=None                            # find parameter key
            data=self.db.simple_select(['key'],['parameter'],where="name='"+ls_parametername+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                parkey = self.db.get_new_primary_key('parameter')[0]
                self.db.simple_insert('parameter',['key','name','type','range','listidx'],[parkey,ls_parametername,ls_type,ls_options,asNumber(ls_listidx,'int',0)])   # insert new parameter entry
            else:
                parkey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameter',['type','range','listidx'],[ls_type,ls_options,asNumber(ls_listidx,'int',0)],['key'],[parkey])    # update parameter entry
            # (iii) Create/Modify parameter widget entry in table 'parameterwidget'
            parwdg_key=None                        # find parameter key
            whereclause=self.db.getWhereClause_from_ColumnValues(['parameterwidget'],['key_simulation','key_parameter','name'],[self.simkey,parkey,ls_name])
            data=self.db.simple_select(['key'],['parameterwidget'],where=whereclause)
            if len(data)<=0: # no parameter widget available --> insert new one in table 
                parwdg_key = self.db.get_new_primary_key('parameterwidget')[0]
                self.db.simple_insert('parameterwidget',\
                                      ['key'     ,'key_simulation','key_parameter','name' ,'type'         ,'range' ,'size'  ,'value'],\
                                      [parwdg_key,self.simkey     ,parkey         ,ls_name,'listselection',ls_options,ls_size,ls_value])   # insert new parameter entry
            else:
                parwdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'         ,'range' ,'size' ,'value'],\
                                                 ['listselection',ls_options,ls_size,ls_value], ['key'],[parwdg_key])   # update parameter widget entry
                elif self.parsemode in [self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'         ,'range' ,'size'],\
                                                 ['listselection',ls_options,ls_size], ['key'],[parwdg_key])            # update parameter widget entry except value
                
    def new_checkbox(self,cb_name,cb_options,cb_parametername,cb_value):
        #print("new_checkbox: terms=",cb_name,cb_options,cb_parametername,cb_value)
        # (i) prepare parameters
        if self.db!=None:
            # (ii) Create/Modify parameter entry in table 'parameter'
            parkey=None                            # find parameter key
            data=self.db.simple_select(['key'],['parameter'],where="name='"+cb_parametername+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                parkey = self.db.get_new_primary_key('parameter')[0]
                self.db.simple_insert('parameter',['key','name','type','range'],[parkey,cb_parametername,'text',cb_options])   # insert new parameter entry
            else:
                parkey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameter',['type','range'],['text',cb_options],['key'],[parkey])    # update parameter entry
            # (iii) Create/Modify parameter widget entry in table 'parameterwidget'
            parwdg_key=None                        # find parameter key
            whereclause=self.db.getWhereClause_from_ColumnValues(['parameterwidget'],['key_simulation','key_parameter','name'],[self.simkey,parkey,cb_name])
            data=self.db.simple_select(['key'],['parameterwidget'],where=whereclause)
            if len(data)<=0: # no parameter widget available --> insert new one in table 
                parwdg_key = self.db.get_new_primary_key('parameterwidget')[0]
                self.db.simple_insert('parameterwidget',\
                                      ['key'     ,'key_simulation','key_parameter','name' ,'type'    ,'range'   ,'value'],\
                                      [parwdg_key,self.simkey     ,parkey         ,cb_name,'checkbox',cb_options,cb_value])   # insert new parameter entry
            else:
                parwdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'    ,'range'   ,'value'],\
                                                 ['checkbox',cb_options,cb_value], ['key'],[parwdg_key])   # update parameter widget entry
                elif self.parsemode in [self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'    ,'range'],\
                                                 ['checkbox',cb_options], ['key'],[parwdg_key])            # update parameter widget entry except value
                
    def new_radiobutton(self,rb_name,rb_options,rb_parametername,rb_value):
        #print("new_radiobutton: terms=",rb_name,rb_options,rb_parametername,rb_value)
        # (i) prepare parameters
        if self.db!=None:
            # (ii) Create/Modify parameter entry in table 'parameter'
            parkey=None                            # find parameter key
            data=self.db.simple_select(['key'],['parameter'],where="name='"+rb_parametername+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                parkey = self.db.get_new_primary_key('parameter')[0]
                self.db.simple_insert('parameter',['key','name','type','range'],[parkey,rb_parametername,'text',rb_options])   # insert new parameter entry
            else:
                parkey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameter',['type','range'],['text',rb_options],['key'],[parkey])    # update parameter entry
            # (iii) Create/Modify parameter widget entry in table 'parameterwidget'
            parwdg_key=None                        # find parameter key
            whereclause=self.db.getWhereClause_from_ColumnValues(['parameterwidget'],['key_simulation','key_parameter','name'],[self.simkey,parkey,rb_name])
            data=self.db.simple_select(['key'],['parameterwidget'],where=whereclause)
            if len(data)<=0: # no parameter widget available --> insert new one in table 
                parwdg_key = self.db.get_new_primary_key('parameterwidget')[0]
                self.db.simple_insert('parameterwidget',\
                                      ['key'     ,'key_simulation','key_parameter','name' ,'type'       ,'range'   ,'value'],\
                                      [parwdg_key,self.simkey     ,parkey         ,rb_name,'radiobutton',rb_options,rb_value])   # insert new parameter entry
            else:
                parwdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'       ,'range'   ,'value'],\
                                                 ['radiobutton',rb_options,rb_value], ['key'],[parwdg_key])   # update parameter widget entry
                elif self.parsemode in [self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'       ,'range'],\
                                                 ['radiobutton',rb_options], ['key'],[parwdg_key])            # update parameter widget entry except value
                
    def new_button(self,rb_name,rb_labeltext_buttontext,rb_parametername):
        #print("new_button: terms=",rb_name,rb_labeltext_buttontext,rb_parametername)
        # (i) prepare parameters
        if self.db!=None:
            # (ii) Create/Modify parameter entry in table 'parameter'
            parkey=None                            # find parameter key
            data=self.db.simple_select(['key'],['parameter'],where="name='"+rb_parametername+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                parkey = self.db.get_new_primary_key('parameter')[0]
                self.db.simple_insert('parameter',['key','name','type','range'],[parkey,rb_parametername,'text',rb_labeltext_buttontext])   # insert new parameter entry
            else:
                parkey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameter',['type','range'],['text',rb_labeltext_buttontext],['key'],[parkey])            # update parameter entry
            # (iii) Create/Modify parameter widget entry in table 'parameterwidget'
            parwdg_key=None                        # find parameter key
            whereclause=self.db.getWhereClause_from_ColumnValues(['parameterwidget'],['key_simulation','key_parameter','name'],[self.simkey,parkey,rb_name])
            data=self.db.simple_select(['key'],['parameterwidget'],where=whereclause)
            if len(data)<=0: # no parameter widget available --> insert new one in table 
                parwdg_key = self.db.get_new_primary_key('parameterwidget')[0]
                self.db.simple_insert('parameterwidget',\
                                      ['key'     ,'key_simulation','key_parameter','name' ,'type'  ,'range'                ,'value'],\
                                      [parwdg_key,self.simkey     ,parkey         ,rb_name,'button',rb_labeltext_buttontext,'0'])      # insert new parameter entry
            else:
                parwdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'  ,'range'                ,'value'],\
                                                 ['button',rb_labeltext_buttontext,'0'    ], ['key'],[parwdg_key])   # update parameter widget entry (value is here irrelevant as set to '0')
                
    def new_textin(self,txi_name,txi_size,txi_parametername,txi_listidx,txi_value):
        #print("new_textin: terms=",txi_name,txi_size,txi_parametername,txi_listidx,txi_value)
        # (i) prepare parameters
        if self.db!=None:
            # (ii) Create/Modify parameter entry in table 'parameter'
            parkey=None                            # find parameter key
            data=self.db.simple_select(['key'],['parameter'],where="name='"+txi_parametername+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                parkey = self.db.get_new_primary_key('parameter')[0]
                self.db.simple_insert('parameter',['key','name','type','range','listidx'],[parkey,txi_parametername,'text','None',asNumber(txi_listidx,'int',0)])   # insert new parameter entry
            else:
                parkey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameter',['type','range','listidx'],['text','None',asNumber(txi_listidx,'int',0)],['key'],[parkey])    # update parameter entry
            # (iii) Create/Modify parameter widget entry in table 'parameterwidget'
            parwdg_key=None                        # find parameter key
            whereclause=self.db.getWhereClause_from_ColumnValues(['parameterwidget'],['key_simulation','key_parameter','name'],[self.simkey,parkey,txi_name])
            data=self.db.simple_select(['key'],['parameterwidget'],where=whereclause)
            if len(data)<=0: # no parameter widget available --> insert new one in table 
                parwdg_key = self.db.get_new_primary_key('parameterwidget')[0]
                self.db.simple_insert('parameterwidget',\
                                      ['key'     ,'key_simulation','key_parameter','name'  ,'type'     ,'range' ,'size'  ,'value'],\
                                      [parwdg_key,self.simkey     ,parkey         ,txi_name,'textfield','None'  ,txi_size,txi_value])   # insert new parameter entry
            else:
                parwdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'     ,'range','size'  ,'value'  ],\
                                                 ['textfield','None' ,txi_size,txi_value], ['key'],[parwdg_key])   # update parameter widget entry
                elif self.parsemode in [self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('parameterwidget',\
                                                 ['type'     ,'range','size'],\
                                                 ['textfield','None' ,txi_size], ['key'],[parwdg_key])             # update parameter widget entry except value
                
    def new_image(self,img_name,img_scale,img_range,img_dataname,img_type):
        #print("new_image: terms=",img_name,img_scale,img_range,img_dataname,img_type)
        # (i) prepare parameters
        if img_type in ['int','INT','integer','INTEGER']: img_type='int'
        if img_type in ['float','FLOAT','double','DOUBLE']: img_type='float'
        if img_type in ['binary','bool','boolean','BINARY','BOOL','BOOLEAN']: img_type='binary'
        if self.db!=None:
            # (ii) Create/Modify dataarray entry in table 'dataarray'
            datakey=None                            # find dataarray key
            data=self.db.simple_select(['key'],['dataarray'],where="name='"+img_dataname+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                datakey = self.db.get_new_primary_key('dataarray')[0]
                self.db.simple_insert('dataarray',['key','name','type','range'],[datakey,img_dataname,img_type,img_range])  # insert new dataarray entry
            else:
                datakey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('dataarray',['type','range'],[img_type,img_range],['key'],[datakey])           # update dataarray entry
            # (iii) Create/Modify data widget entry in table 'datawidget'
            datawdg_key=None                        # find data widget key
            whereclause=self.db.getWhereClause_from_ColumnValues(['datawidget'],['key_simulation','key_dataarray','name'],[self.simkey,datakey,img_name])
            data=self.db.simple_select(['key'],['datawidget'],where=whereclause)
            if len(data)<=0: # no data widget available --> insert new one in table 
                datawdg_key = self.db.get_new_primary_key('datawidget')[0]
                self.db.simple_insert('datawidget',\
                                      ['key'      ,'key_simulation','key_dataarray','name'  ,'type'  ,'range'  ,'scale'],\
                                      [datawdg_key,self.simkey     ,datakey        ,img_name,'image' ,img_range,img_scale])   # insert new parameter entry
            else:
                datawdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('datawidget',\
                                                 ['type' ,'range'  ,'scale'  ],\
                                                 ['image',img_range,img_scale], ['key'],[datawdg_key])                        # update parameter widget entry
                
    def new_textout(self,txo_name,txo_size,txo_options,txo_dataname):
        #print("new_textout: terms=",txo_name,txo_size,txo_dataname)
        # (i) prepare parameters
        options_list=parseStringAsList(txo_options,'string',['None'])    # just for checking and normalizing
        txo_options=str(options_list)
        txo_options=txo_options.replace("'","")                          # remove quotes
        txo_options=txo_options.replace('"','')                          # remove quotes 
        if self.db!=None:
            # (ii) Create/Modify dataarray entry in table 'dataarray'
            datakey=None                            # find dataarray key
            data=self.db.simple_select(['key'],['dataarray'],where="name='"+txo_dataname+"'")
            if len(data)<=0: # no parameter with this name --> insert new one in table
                datakey = self.db.get_new_primary_key('dataarray')[0]
                self.db.simple_insert('dataarray',['key','name','type','range'],[datakey,txo_dataname,'text','None'])   # insert new dataarray entry
            else:
                datakey=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('dataarray',['type','range'],['text','None'],['key'],[datakey])        # update dataarray entry
            # (iii) Create/Modify data widget entry in table 'datawidget'
            datawdg_key=None                        # find data widget key
            whereclause=self.db.getWhereClause_from_ColumnValues(['datawidget'],['key_simulation','key_dataarray','name'],[self.simkey,datakey,txo_name])
            data=self.db.simple_select(['key'],['datawidget'],where=whereclause)
            if len(data)<=0: # no data widget available --> insert new one in table 
                datawdg_key = self.db.get_new_primary_key('datawidget')[0]
                self.db.simple_insert('datawidget',\
                                      ['key'      ,'key_simulation','key_dataarray','name'  ,'type'     ,'range'    ,'scale'],\
                                      [datawdg_key,self.simkey     ,datakey        ,txo_name,'textfield',txo_options,1.0])   # insert new data widget entry
            else:
                datawdg_key=data[0][0]
                if self.parsemode in [self.PARSEMODE_UpdateOld,self.PARSEMODE_UpdateOldExceptValues]:
                    self.db.simple_update_byPKEY('datawidget',\
                                                 ['type'     ,'range'    ,'scale'],\
                                                 ['textfield',txo_options,1.0    ], ['key'],[datawdg_key])   # update data widget entry
                
if __name__ == '__main__':
    print("\nModule Test ivisit.parser (A.Knoblauch, 15/9/2019)") 
    print("---------------------------------------------------\n") 
    pr = IVisitParser("dummyscripttoparse.py") 

