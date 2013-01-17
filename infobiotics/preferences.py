from traits.etsconfig.api import ETSConfig
from apptools.preferences.api import ScopedPreferences, set_default_preferences, get_default_preferences 
import os
import sys

ETSConfig.company = 'Infobiotics'

preferences = ScopedPreferences(filename=os.path.join(ETSConfig.get_application_data(create=True), 'preferences.ini'))
set_default_preferences(preferences) # allows use of Preferences, PreferencesHelper and bind_preference without explicitly passing preferences
assert preferences == get_default_preferences()

from infobiotics.mcss.mcss_preferences import PREFERENCES_PATH as MCSS_PREFERENCES_PATH
from infobiotics.mcsscmaes.mcsscmaes_preferences import PREFERENCES_PATH as MCSSCMAES_PREFERENCES_PATH
from infobiotics.pmodelchecker.pmodelchecker_preferences import PREFERENCES_PATH as PMODELCHECKER_PREFERENCES_PATH
from infobiotics.pmodelchecker.prism.prism_preferences import PREFERENCES_PATH as PRISM_PREFERENCES_PATH
from infobiotics.pmodelchecker.mc2.mc2_preferences import PREFERENCES_PATH as MC2_PREFERENCES_PATH
from infobiotics.pmodelchecker.mc2.mc2_preferences import MC2_MCSS_PREFERENCES_PATH
from infobiotics.poptimizer.poptimizer_preferences import PREFERENCES_PATH as POPTIMIZER_PREFERENCES_PATH

DEFAULT_MCSS_EXECUTABLE = 'default/'+MCSS_PREFERENCES_PATH+'.executable'
DEFAULT_MCSSCMAES_EXECUTABLE = 'default/'+MCSSCMAES_PREFERENCES_PATH+'.executable'
DEFAULT_PMODELCHECKER_EXECUTABLE = 'default/'+PMODELCHECKER_PREFERENCES_PATH+'.executable'
DEFAULT_PRISM_EXECUTABLE = 'default/'+PRISM_PREFERENCES_PATH+'.executable'
DEFAULT_MC2_EXECUTABLE = 'default/'+MC2_PREFERENCES_PATH+'.executable'
DEFAULT_MC2_MCSS_EXECUTABLE = 'default/'+MC2_MCSS_PREFERENCES_PATH+'.executable'
DEFAULT_POPTIMIZER_EXECUTABLE = 'default/'+POPTIMIZER_PREFERENCES_PATH+'.executable'

if sys.platform.startswith('win'):
    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'mcss.exe'),
    preferences.set(DEFAULT_MCSSCMAES_EXECUTABLE, 'mcss-cmaes.exe'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, 'pmodelchecker.exe'),
    preferences.set(DEFAULT_PRISM_EXECUTABLE, 'pmodelchecker.exe'),
    preferences.set(DEFAULT_MC2_EXECUTABLE, 'pmodelchecker.exe'),
    preferences.set(DEFAULT_MC2_MCSS_EXECUTABLE, 'mcss.exe'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, 'poptimizer.exe'),
else:
    # RelativeFile traits use Which module to find files on the PATH so we don't
    # need to hard code paths like this: 
    #     preferences.set(DEFAULT_MCSS_EXECUTABLE, '/usr/bin/mcss'),
    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'mcss'),
    preferences.set(DEFAULT_MCSSCMAES_EXECUTABLE, 'mcss-cmaes'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, 'pmodelchecker'),
    preferences.set(DEFAULT_PRISM_EXECUTABLE, 'pmodelchecker'),
    preferences.set(DEFAULT_MC2_EXECUTABLE, 'pmodelchecker'),
    preferences.set(DEFAULT_MC2_MCSS_EXECUTABLE, 'mcss'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, 'poptimizer'),

#default_directory = os.getcwd()
default_directory = os.path.expanduser('~')
preferences.set('default/'+MCSS_PREFERENCES_PATH+'.directory', default_directory)
preferences.set('default/'+MCSSCMAES_PREFERENCES_PATH+'.directory', default_directory)
preferences.set('default/'+PMODELCHECKER_PREFERENCES_PATH+'.directory', default_directory)
preferences.set('default/'+PRISM_PREFERENCES_PATH+'.directory', default_directory)
preferences.set('default/'+MC2_PREFERENCES_PATH+'.directory', default_directory)
preferences.set('default/'+MC2_MCSS_PREFERENCES_PATH+'.directory', default_directory)
preferences.set('default/'+POPTIMIZER_PREFERENCES_PATH+'.directory', default_directory)

#preferences.set('default/envisage.ui.workbench.prompt_on_exit', False)

# uncomment to make scope 'default' non-transient
#preferences.get_scope('default').filename = os.path.join(ETSConfig.get_application_data(create=True), 'default_preferences.ini')
#print default_preferences.filename
#preferences.flush()
#preferences.save()

if __name__ == '__main__':
    preferences.dump()
##    print
##    print "'%s'" % preferences.get('mcsscmaes.executable')
##    print
##    name = 'mcss'
##    for key in preferences.node(name).keys():
##        print '.'.join([name, key])
#    pmodelchecker_executable_name = "%s" % preferences.get('pmodelchecker.executable')
#    from infobiotics.thirdparty.which import which
#    print which(pmodelchecker_executable_name)
    