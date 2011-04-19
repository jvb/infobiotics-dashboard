from infobiotics.pmodelchecker.pmodelchecker_preferences import PModelCheckerParamsPreferencesHelper, PModelCheckerParamsPreferencesPage, RelativeFile
import sys

#TODO copy this pattern for all ParamsPreferences (and maybe Params) subclasses
name = 'mc2.exe' if sys.platform.startswith('win') else 'mc2' 
MC2Executable = RelativeFile(name, filter=name, absolute=True, auto_set=True, executable=True) # executable=True implies exists=True

class MC2ParamsPreferencesHelper(PModelCheckerParamsPreferencesHelper):
    mc2_executable = MC2Executable 

class MC2ParamsPreferencesPage(PModelCheckerParamsPreferencesPage):
    mc2_executable = MC2Executable
