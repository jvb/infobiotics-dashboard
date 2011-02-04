from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage, RelativeFile
import sys

PREFERENCES_PATH = 'mcss' #TODO

#TODO copy this pattern for all ParamsPreferences (and maybe Params) subclasses
name = 'mcss.exe' if sys.platform.startswith('win') else 'mcss' 
McssExecutable = RelativeFile(name, filter=name, absolute=True, auto_set=True, executable=True) # executable=True implies exists=True

class McssParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH
    executable = McssExecutable 

class McssParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
    executable = McssExecutable

    # uses ParamsPreferencesPage view
    
