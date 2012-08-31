from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage, RelativeFile
import sys
#from enthought.traits.api import Int

PREFERENCES_PATH = 'pmodelchecker'
name = 'pmodelchecker.exe' if sys.platform.startswith('win') else 'pmodelchecker' 
PModelCheckerExecutable = RelativeFile(name, filter=name, absolute=False, auto_set=True, executable=True) # executable=True implies exists=True

class PModelCheckerParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH
    executable = PModelCheckerExecutable 
#    directory = Int #TODO why do PRISM and MC2 share directory
    
class PModelCheckerParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
    executable = PModelCheckerExecutable
    

    # uses ParamsPreferencesPage view
    
if __name__ == '__main__':
    helper = PModelCheckerParamsPreferencesHelper()
    print helper.executable
