# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: mcss_ui_plugin.py 120 2009-12-08 14:48:20Z jvb $
# $HeadURL: svn+ssh://infobiotics.dyndns.org/svn/infobiotics/Infobiotics Dashboard/trunk/infobiotics/workbench/plugins/mcss/mcss_ui_plugin.py $
# $Author: jvb $
# $Revision: 120 $
# $Date: 2009-12-08 14:48:20 +0000 (Tue, 08 Dec 2009) $


from enthought.envisage.api import Plugin
from enthought.traits.api import List
#from enthought.pyface.workbench.api import Perspective, PerspectiveItem
from action_set import SimulatorResultsActionSet


class SimulatorResultsUIPlugin(Plugin):

    # 'IPlugin' interface
    id = 'infobiotics.dashboard.plugins.simulator_results.ui_plugin.SimulatorResultsUIPlugin' # The plugin's unique identifier
    name = 'SimulatorResults' # The plugin's name (suitable for displaying to the user)

    # Contributions to extension points made by this plugin

    action_sets = List(contributes_to='enthought.envisage.ui.workbench.action_sets')
    def _action_sets_default(self):
        return [SimulatorResultsActionSet]

#    #TODO H5 opener
#    openers = List(contributes_to='infobiotics.dashboard.plugins.unified_open_action.unified_open_action_plugin.openers')
#    def _openers_default(self):
#        from openers import openers
#        return openers
