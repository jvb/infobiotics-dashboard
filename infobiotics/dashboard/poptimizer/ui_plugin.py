from enthought.envisage.api import Plugin
from enthought.traits.api import List
from enthought.pyface.workbench.api import Perspective, PerspectiveItem
from action_set import POptimizerActionSet

class POptimizerUIPlugin(Plugin):
    id = 'infobiotics.dashboard.plugins.poptimizer.ui_plugin'
    name = 'POptimizer'

    # Contributions to extension points made by this plugin
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
        return []
