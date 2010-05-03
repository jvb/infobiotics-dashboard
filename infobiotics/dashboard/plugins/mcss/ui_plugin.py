# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: ui_plugin.py 405 2010-01-25 13:13:07Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/mcss/ui_plugin.py $
# $Author: jvb $
# $Revision: 405 $
# $Date: 2010-01-25 13:13:07 +0000 (Mon, 25 Jan 2010) $


from enthought.envisage.api import Plugin
from enthought.traits.api import List
from enthought.pyface.workbench.api import Perspective, PerspectiveItem

from action_set import McssActionSet
from preferences_page import McssPreferencesPage


class McssUIPlugin(Plugin):

    # 'IPlugin' interface
    id = 'infobiotics.dashboard.mcss.ui_plugin.McssUIPlugin' # The plugin's unique identifier
    name = 'mcss' # The plugin's name (suitable for displaying to the user)

    # Contributions to extension points made by this plugin

    action_sets = List(contributes_to='enthought.envisage.ui.workbench.action_sets')
    def _action_sets_default(self):
        return [McssActionSet]

#    perspectives = List(contributes_to='enthought.envisage.ui.workbench.perspectives')
#    def _perspectives_default(self):
#        return []
#
#    views = List(contributes_to='enthought.envisage.ui.workbench.views')
#    def _views_default(self):
#        return []
#
    preferences_pages = List(contributes_to='enthought.envisage.ui.workbench.preferences_pages')
    def _preferences_pages_default(self):
        return [McssPreferencesPage]

    openers = List(contributes_to='infobiotics.dashboard.plugins.unified_open_action.unified_open_action_plugin.openers')
    def _openers_default(self):
        from openers import openers
        return openers
    
    experiments = List(contributes_to='infobiotics.dashboard.plugins.experiments.ui_plugin.experiments') #TODO
    def _experiments_default(self):
        from mcss_experiment import McssExperiment
        return McssExperiment()
