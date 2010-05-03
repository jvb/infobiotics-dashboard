from enthought.etsconfig.api import ETSConfig 

# set toolkit to 'qt4' (TraitsBackendQt) before any Traits imports
ETSConfig.toolkit = 'qt4' # os.environ['ETS_TOOLKIT']='qt4' also works

# use ~/.infobiotics instead of ~/.enthought for preferences.ini
ETSConfig.company = 'infobiotics'

from enthought.preferences.api import set_default_preferences, ScopedPreferences
import os
set_default_preferences(
    ScopedPreferences(
        filename=os.path.join(ETSConfig.application_data, 'preferences.ini')
    )
) 
