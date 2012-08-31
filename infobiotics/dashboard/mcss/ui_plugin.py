from enthought.envisage.api import Plugin, contributes_to
from enthought.traits.api import List
from enthought.pyface.workbench.api import Perspective, PerspectiveItem

from action_set import McssActionSet
from infobiotics.mcss.mcss_preferences import McssParamsPreferencesPage

import os
from enthought.etsconfig.api import ETSConfig

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

#    views = List(contributes_to='enthought.envisage.ui.workbench.views')
#    def _views_default(self):
#        return []

    preferences_pages = List(contributes_to='enthought.envisage.ui.workbench.preferences_pages')
    def _preferences_pages_default(self):
        return [McssParamsPreferencesPage]

#    openers = List(contributes_to='infobiotics.dashboard.plugins.unified_open_action.unified_open_action_plugin.openers') #TODO
#    def _openers_default(self):
#        from openers import openers
#        return openers
    
#    experiments = List(contributes_to='infobiotics.dashboard.plugins.experiments.ui_plugin.experiments') #TODO
#    def _experiments_default(self):
#        from mcss_experiment import McssExperiment
#        return McssExperiment()
    
#    # file:///home/jvb/src/ETS_3.4.0/AppTools/docs/html/preferences/PreferencesInEnvisage.html
#    
#    preferences = List(contributes_to='enthought.envisage.preferences')
#    def _preferences_default(self):
#        return ['file://%s' % os.path.join(ETSConfig.application_data, 'preferences.ini')]