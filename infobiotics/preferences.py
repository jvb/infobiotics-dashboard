from enthought.etsconfig.api import ETSConfig
from enthought.preferences.api import ScopedPreferences, set_default_preferences, Preferences
import os.path
import sys

ETSConfig.company = 'Infobiotics'

preferences = ScopedPreferences(filename=os.path.join(ETSConfig.get_application_data(create=True), 'preferences.ini'))

#set_default_preferences(preferences)

DEFAULT_MCSS_EXECUTABLE = 'default/mcss.executable'
DEFAULT_PMODELCHECKER_EXECUTABLE = 'default/pmodelchecker.executable'
DEFAULT_POPTIMIZER_EXECUTABLE = 'default/poptimizer.executable'

if sys.platform.startswith('linux'):
    preferences.set(DEFAULT_MCSS_EXECUTABLE, '/usr/bin/mcss'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, '/usr/bin/pmodelchecker'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, '/usr/bin/poptimizer'),

elif sys.platform.startswith('win'):
    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'C:\\Program Files\\Infobiotics-Workbench\\infobiotics-workbench\\mcss.EXE'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, 'C:\\Program Files\\Infobiotics-Workbench\\infobiotics-workbench\\pmodelchecker.EXE'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, 'C:\\Program Files\\Infobiotics-Workbench\\infobiotics-workbench\\poptimizer.EXE'),
    #TODO directory as well? Might be better here than in Params._directory_default()?

elif sys.platform.startswith('darwin'):
    preferences.set(DEFAULT_MCSS_EXECUTABLE, '/Application/InfobioticsWorkbench/mcss'), #TODO check these
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, '/Application/InfobioticsWorkbench/pmodelchecker'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, '/Application/InfobioticsWorkbench/poptimizer'),

else:
    raise ValueError('Not running on Windows, Mac or Linux!')

# uncomment to make scope 'default' non-transient
#preferences.get_scope('default').filename = os.path.join(ETSConfig.get_application_data(create=True), 'default_preferences.ini')
#print default_preferences.filename
#preferences.flush() # save preferences


if __name__ == '__main__':
    preferences.dump()
