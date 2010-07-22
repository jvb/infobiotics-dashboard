from enthought.envisage.api import Plugin#, contributes_to
from enthought.traits.api import List
#from enthought.pyface.workbench.api import Perspective, PerspectiveItem
from action_set import PModelCheckerActionSet

class PModelCheckerUIPlugin(Plugin):
    id = 'infobiotics.dashboard.plugins.pmodelchecker.ui_plugin.PModelCheckerUIPlugin'
    name = 'pmodelchecker'

    action_sets = List(contributes_to='enthought.envisage.ui.workbench.action_sets')
    perspectives = List(contributes_to='enthought.envisage.ui.workbench.perspectives')
    views = List(contributes_to='enthought.envisage.ui.workbench.views')
    preferences_pages = List(contributes_to='enthought.envisage.ui.workbench.preferences_pages')

    def _action_sets_default(self):
        return [PModelCheckerActionSet]

    def _perspectives_default(self):
        return []

    def _views_default(self):
        return []

    def _preferences_pages_default(self):
#        from preferences_page import PModelCheckerPreferencesPage
#        return [PModelCheckerPreferencesPage]
        return []

    #TODO plugin-local preferences?
#    preferences = List(
#        ['pkgfile://infobiotics.dashboard.plugins.pmodelchecker/preferences.ini'], 
#        contributes_to='enthought.envisage.preferences'
#    )
