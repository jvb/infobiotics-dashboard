'''
see:
file:///home/jvb/src/ETS_3.3.1/AppTools_3.3.1/docs/html/preferences/PreferencesInEnvisage.html
file:///home/jvb/src/ETS_3.3.1/EnvisageCore_3.1.2/docs/html/preferences.html
https://svn.enthought.com/enthought/browser/AppTools/trunk/examples/preferences/preferences_manager.py
'''

from apptools.preferences.ui.api import PreferencesPage
from traits.api import File
from traitsui.api import View

class CorePreferencesPage(PreferencesPage):

    category = '' # The page's category (e.g. 'General/Appearance'). The empty string means that this is a top-level page.
    name = 'General' # The page name (this is what is shown in the preferences dialog)

    preferences_path = 'infobiotics.dashboard.plugins.core'

#    # Preferences
#    path_to_mcss = File('/usr/bin/mcss')
#
#    # View
#    traits_view = View('path_to_mcss')
    