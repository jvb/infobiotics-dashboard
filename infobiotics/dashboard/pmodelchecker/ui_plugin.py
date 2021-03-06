from envisage.api import Plugin#, contributes_to
from traits.api import List
#from pyface.workbench.api import Perspective, PerspectiveItem
from action_set import PModelCheckerActionSet
from infobiotics.pmodelchecker.pmodelchecker_preferences import PModelCheckerParamsPreferencesPage

class PModelCheckerUIPlugin(Plugin):
    id = 'infobiotics.dashboard.pmodelchecker.ui_plugin.PModelCheckerUIPlugin'
    name = 'pmodelchecker'

    action_sets = List(contributes_to='envisage.ui.workbench.action_sets')
    perspectives = List(contributes_to='envisage.ui.workbench.perspectives')
    views = List(contributes_to='envisage.ui.workbench.views')
    preferences_pages = List(contributes_to='envisage.ui.workbench.preferences_pages')

    def _action_sets_default(self):
        return [PModelCheckerActionSet]

    def _perspectives_default(self):
        return []

    def _views_default(self):
        return []

    def _preferences_pages_default(self):
        return [PModelCheckerParamsPreferencesPage]

    #TODO plugin-local preferences?
#    preferences = List(
#        ['pkgfile://infobiotics.dashboard.pmodelchecker/preferences.ini'], 
#        contributes_to='envisage.preferences'
#    )
