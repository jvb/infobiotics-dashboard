from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
ETSConfig.company = 'Infobiotics'

#print ETSConfig.application_home # /home/jvb/.infobiotics/package/
#print ETSConfig.application_data # /home/jvb/.infobiotics/
#print ETSConfig.user_data # /home/jvb/infobiotics/

from enthought.preferences.api import (
    Preferences, ScopedPreferences,
    get_default_preferences, set_default_preferences,
    PreferencesHelper, 
)
from enthought.preferences.ui.api import PreferencesManager, PreferencesPage

default_preferences_filename = 'default.ini'

# will be done the first time preferences is imported
set_default_preferences(ScopedPreferences(filename=default_preferences_filename))

PreferencesHelper.preferencess = get_default_preferences


#ETSConfig.user_data = '/tmp' #TODO give user change to define user_data in preferences


from enthought.preferences.api import (
    PreferencesHelper, 
)
from commons.traits.api import RelativeFile
from commons.api import which

class McssPreferencesHelper(PreferencesHelper):
    preferences_path = 'infobiotics.mcss'
    
    executable = RelativeFile(absolute=True, executable=True)
    
    def _executable_default(self):
        return which('mcss')


if __name__ == '__main__':
    
    preferences = get_default_preferences()
    #preferences.set('infobiotics.mcss.executable', '/usr/local/bin/mcss')
    helper = McssPreferencesHelper() # raises TraitError if '/usr/local/bin/mcss' doesn't exist
    #print helper.executable
    
    
    #preferences.dump()
