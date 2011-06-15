from infobiotics.pmodelchecker.pmodelchecker_preferences import PModelCheckerParamsPreferencesHelper, PModelCheckerParamsPreferencesPage, RelativeFile, PModelCheckerExecutable
import sys
from enthought.traits.ui.api import View, Group, Item

name = 'prism.bat' if sys.platform.startswith('win') else 'prism' 
PRISMExecutable = RelativeFile(name, filter=name, absolute=False, auto_set=True, executable=True) # executable=True implies exists=True

class PRISMParamsPreferencesHelper(PModelCheckerParamsPreferencesHelper):
    preferences_path = 'prism'
    prism_executable = PRISMExecutable
    executable = PModelCheckerExecutable

class PRISMParamsPreferencesPage(PModelCheckerParamsPreferencesPage):
    preferences_path = 'prism'
    prism_executable = PRISMExecutable
    executable = PModelCheckerExecutable
    
    view = View(
        Group(
            Item('executable', label='PModelChecker executable'),
            Item('prism_executable', label='PRISM executable'),
            show_border=True,
        ),
    )
    