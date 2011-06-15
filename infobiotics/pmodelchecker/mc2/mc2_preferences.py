from infobiotics.pmodelchecker.pmodelchecker_preferences import PModelCheckerParamsPreferencesHelper, PModelCheckerParamsPreferencesPage, RelativeFile, PModelCheckerExecutable
import sys
from enthought.traits.ui.api import View, Group, Item

name = 'mc2.bat' if sys.platform.startswith('win') else 'mc2' 
MC2Executable = RelativeFile(name, filter=name, absolute=False, auto_set=True, executable=True) # executable=True implies exists=True

class MC2ParamsPreferencesHelper(PModelCheckerParamsPreferencesHelper):
    preferences_path = 'mc2'
    mc2_executable = MC2Executable
    executable = PModelCheckerExecutable

class MC2ParamsPreferencesPage(PModelCheckerParamsPreferencesPage):
    preferences_path = 'mc2'
    mc2_executable = MC2Executable
    executable = PModelCheckerExecutable

    view = View(
        Group(
            Item('executable', label='PModelChecker executable'),
            Item('mc2_executable', label='MC2 executable'),
            show_border=True,
        ),
    )
    
    
if __name__ == '__main__':
    helper = MC2ParamsPreferencesHelper()
    print helper.executable    
    