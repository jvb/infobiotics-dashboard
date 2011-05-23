from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage, RelativeFile
import sys

PREFERENCES_PATH = 'mcss'

name = 'mcss.exe' if sys.platform.startswith('win') else 'mcss' 
McssExecutable = RelativeFile(name, filter=name, absolute=False, auto_set=True, executable=True) # executable=True implies exists=True

class McssParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH
    executable = McssExecutable 

class McssParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
    executable = McssExecutable

    # uses ParamsPreferencesPage view
    
