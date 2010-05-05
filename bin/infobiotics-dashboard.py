#!/usr/bin/env python

## from infobiotics/__init__.py
#
#from enthought.etsconfig.api import ETSConfig 
#ETSConfig.toolkit = 'qt4' # os.environ['ETS_TOOLKIT']='qt4' also works
## set toolkit to 'qt4' (TraitsBackendQt) before any Traits imports
#
#ETSConfig.company = 'infobiotics'
## use ~/.infobiotics (or "Application Data\infobiotics") instead of 
## ~/.enthought for preferences.ini
#
#import os.path
#from enthought.preferences.api import (
#    set_default_preferences, ScopedPreferences, get_default_preferences,
#) 
#
#preferences_file_name = os.path.join(ETSConfig.application_data, 'preferences.ini') 
#print "Using preferences file '%s'" % preferences_file_name 
#preferences = ScopedPreferences(filename=preferences_file_name)
#
#import platform
#if platform.system() == 'Windows':
#    preferences.set('mcss._params_program_file', 'C:\\Program Files\\Infobiotics-Workbench\\infobiotics-workbench\\mcss.EXE'),
#    preferences.set('pmodelchecker._params_program_file', 'C:\\Program Files\\Infobiotics-Workbench\\infobiotics-workbench\\pmodelchecker.EXE'),
#    preferences.set('mcss._params_program_file', 'C:\\Program Files\\Infobiotics-Workbench\\infobiotics-workbench\\poptimizer.EXE'),
#
#set_default_preferences(preferences)

import infobiotics.dashboard.run as run
run.main()