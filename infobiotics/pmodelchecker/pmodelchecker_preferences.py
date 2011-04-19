from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage, RelativeFile
import sys

PREFERENCES_PATH = 'pmodelchecker' #TODO

#TODO copy this pattern for all ParamsPreferences (and maybe Params) subclasses
name = 'pmodelchecker.exe' if sys.platform.startswith('win') else 'pmodelchecker' 
PModelCheckerExecutable = RelativeFile(name, filter=name, absolute=True, auto_set=True, executable=True) # executable=True implies exists=True

class PModelCheckerParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH
    executable = PModelCheckerExecutable 

class PModelCheckerParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
    executable = PModelCheckerExecutable

    # uses ParamsPreferencesPage view
    
if __name__ == '__main__':
    helper = PModelCheckerParamsPreferencesHelper()
    print helper.executable
