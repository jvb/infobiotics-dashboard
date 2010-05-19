from enthought.preferences.api import PreferencesHelper
from infobiotics.commons.traits.api import RelativeFile, RelativeDirectory

class ParamsPreferencesHelper(PreferencesHelper):
    ''' Traits-based type checking and conversion from ini format files.'''
    _params_program = RelativeFile(absolute=True, executable=True)#, auto_set=True
    _cwd = RelativeDirectory(absolute=True)#, exists=True#, auto_set=True 
