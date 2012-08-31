from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage, RelativeFile
import sys

PREFERENCES_PATH = 'poptimizer'

name = 'poptimizer.exe' if sys.platform.startswith('win') else 'poptimizer' 
POptimizerExecutable = RelativeFile(name, filter=name, absolute=False, auto_set=True, executable=True) # executable=True implies exists=True

class POptimizerParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH
    executable = POptimizerExecutable 

class POptimizerParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
    executable = POptimizerExecutable

