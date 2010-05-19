'''
see:
file:///home/jvb/src/ETS_3.3.1/AppTools_3.3.1/docs/html/preferences/PreferencesInEnvisage.html
file:///home/jvb/src/ETS_3.3.1/EnvisageCore_3.1.2/docs/html/preferences.html
https://svn.enthought.com/enthought/browser/AppTools/trunk/examples/preferences/preferences_manager.py
'''

from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.api import File
from enthought.traits.ui.api import View


class McssPreferencesPage(PreferencesPage):

    # 'PreferencesPage' interface
    category = '' # The page's category (e.g. 'General/Appearance'). The empty string means that this is a top-level page.
    help_id = 'McssPreferencesPage.help_id' # The page's help identifier (optional). If a help Id *is* provided then there will be a 'Help' button shown on the preference page.
    name = 'mcss' # The page name (this is what is shown in the preferences dialog)

    preferences_path = 'infobiotics.dashboard.plugins.mcss' # The path to the preference node that contains the preferences #TODO does this get used?

    # Preferences
    path_to_mcss = File('/usr/bin/mcss') #TODO

    # View
    traits_view = View('path_to_mcss')
    