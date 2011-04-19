from infobiotics.pmodelchecker.pmodelchecker_preferences import PModelCheckerParamsPreferencesHelper, PModelCheckerParamsPreferencesPage, RelativeFile
import sys

#TODO copy this pattern for all ParamsPreferences (and maybe Params) subclasses
name = 'prism.exe' if sys.platform.startswith('win') else 'prism' 
PRISMExecutable = RelativeFile(name, filter=name, absolute=True, auto_set=True, executable=True) # executable=True implies exists=True

class PRISMParamsPreferencesHelper(PModelCheckerParamsPreferencesHelper):
    prism_executable = PRISMExecutable 

class PRISMParamsPreferencesPage(PModelCheckerParamsPreferencesPage):
    prism_executable = PRISMExecutable
