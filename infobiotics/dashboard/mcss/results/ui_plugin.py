from enthought.envisage.api import Plugin
from enthought.traits.api import List
#from enthought.pyface.workbench.api import Perspective, PerspectiveItem
from action_set import McssResultsActionSet


class McssResultsUIPlugin(Plugin):

    # 'IPlugin' interface
    id = 'infobiotics.dashboard.mcss.results.ui_plugin.McssResultsUIPlugin' # The plugin's unique identifier
    name = 'McssResults' # The plugin's name (suitable for displaying to the user)

    # Contributions to extension points made by this plugin

    action_sets = List(contributes_to='enthought.envisage.ui.workbench.action_sets')
    def _action_sets_default(self):
        return [McssResultsActionSet]

#    #TODO H5 opener
#    openers = List(contributes_to='infobiotics.dashboard.plugins.unified_open_action.unified_open_action_plugin.openers')
#    def _openers_default(self):
#        from openers import openers
#        return openers
