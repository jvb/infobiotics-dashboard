from envisage.api import Plugin
from traits.api import List

ACTION_SETS = 'envisage.ui.workbench.action_sets'

class DashboardPlugin(Plugin):

    id = "infobiotics.plugins.dashboard"
    
    name = 'Dashboard plugin'

    action_sets = List(contributes_to=ACTION_SETS)
    def _action_sets_default(self):
        from core_action_set import CoreActionSet
        return [CoreActionSet]
