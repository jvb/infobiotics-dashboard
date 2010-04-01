from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.api import File
from enthought.traits.ui.api import View, Item

class PModelCheckerPreferencesPage(PreferencesPage):
    '''
    see:
    file:///home/jvb/src/ETS_3.3.1/AppTools_3.3.1/docs/html/preferences/PreferencesInEnvisage.html
    file:///home/jvb/src/ETS_3.3.1/EnvisageCore_3.1.2/docs/html/preferences.html
    https://svn.enthought.com/enthought/browser/AppTools/trunk/examples/preferences/preferences_manager.py
    '''

    # 'PreferencesPage' interface
    name = 'Model checking' # The page name (this is what is shown in the preferences dialog)
    preferences_path = 'plugins.pmodelchecker' # The path to the preference node that contains the preferences
    category = '' # The page's category (e.g. 'General/Appearance'). The empty string means that this is a top-level page.
    help_id = '' # The page's help identifier (optional). If a help Id *is* provided then there will be a 'Help' button shown on the preference page.

    # Preferences
    path_to_pmodelchecker = File('/usr/bin/pmodelchecker')
    path_to_prism = File('/usr/bin/prism')    
    path_to_mc2 = File('/usr/bin/MC2.jar')

#    def _path_to_mc2_changed(self):
#        pass
        
    traits_view = View(
        Item('path_to_pmodelchecker', label='Path to PModelChecker'),
        Item('path_to_prism', label='Path to PRISM'),
        Item('path_to_mc2', label='Path to MC2'),
#        resizable=True,
    )