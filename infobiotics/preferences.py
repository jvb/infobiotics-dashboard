from enthought.etsconfig.api import ETSConfig
from enthought.preferences.api import ScopedPreferences, set_default_preferences, get_default_preferences 
import os
import sys

ETSConfig.company = 'Infobiotics'

preferences = ScopedPreferences(filename=os.path.join(ETSConfig.get_application_data(create=True), 'preferences.ini'))
set_default_preferences(preferences) # allows use of Preferences, PreferencesHelper and bind_preference without explicitly passing preferences
assert preferences == get_default_preferences()

DEFAULT_MCSS_EXECUTABLE = 'default/mcss.executable'
DEFAULT_PMODELCHECKER_EXECUTABLE = 'default/pmodelchecker.executable'
DEFAULT_POPTIMIZER_EXECUTABLE = 'default/poptimizer.executable'

if sys.platform.startswith('win'):
    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'mcss.exe'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, 'pmodelchecker.exe'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, 'poptimizer.exe'),
else:
    # RelativeFile traits use Which module to find files on the PATH so we don't
    # need to hard code paths like this: 
    #     preferences.set(DEFAULT_MCSS_EXECUTABLE, '/usr/bin/mcss'),
    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'mcss'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, 'pmodelchecker'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, 'poptimizer'),

preferences.set('default/mcss.directory', os.path.expanduser('~'))
preferences.set('default/pmodelchecker.directory', os.path.expanduser('~'))
preferences.set('default/poptimizer.directory', os.path.expanduser('~'))

##TODO per plugin-style preferences, in the transient 'default' scope 
#import infobiotics.preferences
#from enthought.preferences.api import get_default_preferences 
#preferences = get_default_preferences() or infobiotics.preferences.preferences
#DEFAULT_MCSS_EXECUTABLE = 'default/mcss.executable'
#if sys.platform.startswith('linux'):
#    preferences.set(DEFAULT_MCSS_EXECUTABLE, '/usr/bin/mcss'),
#elif sys.platform.startswith('win'):
#    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'C:\\Program Files\\Infobiotics-Workbench\\infobiotics-workbench\\mcss.EXE'),
#elif sys.platform.startswith('darwin'):
#    preferences.set(DEFAULT_MCSS_EXECUTABLE, '/usr/bin/mcss'), #TODO check these
#else:
#    raise ValueError('Not running on Windows, Mac or Linux!')
#preferences.set('default/mcss.directory', os.getcwd())
    

# uncomment to make scope 'default' non-transient
#preferences.get_scope('default').filename = os.path.join(ETSConfig.get_application_data(create=True), 'default_preferences.ini')
#print default_preferences.filename
#preferences.flush() # save preferences


if __name__ == '__main__':
    preferences.dump()
