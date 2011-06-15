from enthought.etsconfig.api import ETSConfig
from enthought.preferences.api import ScopedPreferences, set_default_preferences, get_default_preferences 
import os
import sys

ETSConfig.company = 'Infobiotics'

preferences = ScopedPreferences(filename=os.path.join(ETSConfig.get_application_data(create=True), 'preferences.ini'))
set_default_preferences(preferences) # allows use of Preferences, PreferencesHelper and bind_preference without explicitly passing preferences
assert preferences == get_default_preferences()

DEFAULT_MCSS_EXECUTABLE = 'default/mcss.executable'
DEFAULT_MCSSCMAES_EXECUTABLE = 'default/mcsscmaes.executable'
DEFAULT_PMODELCHECKER_EXECUTABLE = 'default/pmodelchecker.executable'
DEFAULT_PMODELCHECKER_MC2_EXECUTABLE = 'default/mc2.executable'
DEFAULT_PMODELCHECKER_PRISM_EXECUTABLE = 'default/prism.executable'
DEFAULT_POPTIMIZER_EXECUTABLE = 'default/poptimizer.executable'

if sys.platform.startswith('win'):
    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'mcss.exe'),
    preferences.set(DEFAULT_MCSSCMAES_EXECUTABLE, 'mcss-cmaes.exe'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, 'pmodelchecker.exe'),
    preferences.set(DEFAULT_PMODELCHECKER_MC2_EXECUTABLE, 'pmodelchecker.exe'),
    preferences.set(DEFAULT_PMODELCHECKER_PRISM_EXECUTABLE, 'pmodelchecker.exe'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, 'poptimizer.exe'),
else:
    # RelativeFile traits use Which module to find files on the PATH so we don't
    # need to hard code paths like this: 
    #     preferences.set(DEFAULT_MCSS_EXECUTABLE, '/usr/bin/mcss'),
    preferences.set(DEFAULT_MCSS_EXECUTABLE, 'mcss'),
    preferences.set(DEFAULT_MCSSCMAES_EXECUTABLE, 'mcss-cmaes'),
    preferences.set(DEFAULT_PMODELCHECKER_EXECUTABLE, 'pmodelchecker'),
    preferences.set(DEFAULT_PMODELCHECKER_MC2_EXECUTABLE, 'pmodelchecker'),
    preferences.set(DEFAULT_PMODELCHECKER_PRISM_EXECUTABLE, 'pmodelchecker'),
    preferences.set(DEFAULT_POPTIMIZER_EXECUTABLE, 'poptimizer'),

#default_directory = os.getcwd()
default_directory = os.path.expanduser('~')
preferences.set('default/mcss.directory', default_directory)
preferences.set('default/mcsscmaes.directory', default_directory)
preferences.set('default/pmodelchecker.directory', default_directory)
preferences.set('default/poptimizer.directory', default_directory)

#preferences.set('default/enthought.envisage.ui.workbench.prompt_on_exit', False)

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
    