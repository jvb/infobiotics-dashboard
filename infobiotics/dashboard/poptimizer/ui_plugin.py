from enthought.envisage.api import Plugin
from enthought.traits.api import List
from action_set import POptimizerActionSet
from infobiotics.poptimizer.poptimizer_preferences import POptimizerParamsPreferencesPage

class POptimizerUIPlugin(Plugin):
    id = 'infobiotics.dashboard.poptimizer.ui_plugin'
    name = 'POptimizer'

    action_sets = List(contributes_to='enthought.envisage.ui.workbench.action_sets')
    perspectives = List(contributes_to='enthought.envisage.ui.workbench.perspectives')
    views = List(contributes_to='enthought.envisage.ui.workbench.views')
    preferences_pages = List(contributes_to='enthought.envisage.ui.workbench.preferences_pages')

    def _action_sets_default(self):
        return [POptimizerActionSet]

    def _perspectives_default(self):
        return []

    def _views_default(self):
        return []

    def _preferences_pages_default(self):
        return [POptimizerParamsPreferencesPage]
