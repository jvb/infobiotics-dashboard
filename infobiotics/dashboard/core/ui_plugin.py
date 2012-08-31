from envisage.api import Plugin, contributes_to
from traits.api import List
from pyface.workbench.api import Perspective, PerspectiveItem

from action_set import CoreActionSet

#from preferences_page import CorePreferencesPage
#import os
#from traits.etsconfig.api import ETSConfig

from envisage.plugins.python_shell.python_shell_plugin import PythonShellPlugin
import infobiotics.__version__
from infobiotics.api import *


class CoreUIPlugin(Plugin):

    id = 'infobiotics.dashboard.core.ui_plugin.CoreUIPlugin'
    name = 'Core'

    action_sets = List(contributes_to='envisage.ui.workbench.action_sets')
    def _action_sets_default(self):
        return [CoreActionSet]

#    perspectives = List(contributes_to='envisage.ui.workbench.perspectives')
#    def _perspectives_default(self):
#        return []

#    views = List(contributes_to='envisage.ui.workbench.views')
#    def _views_default(self):
#        return []

#    preferences_pages = List(contributes_to='envisage.ui.workbench.preferences_pages')
#    def _preferences_pages_default(self):
#        return [McssPreferencesPage]

#    openers = List(contributes_to='infobiotics.dashboard.plugins.unified_open_action.unified_open_action_plugin.openers')
#    def _openers_default(self):
#        from openers import openers
#        return openers
#    
#    experiments = List(contributes_to='infobiotics.dashboard.plugins.experiments.ui_plugin.experiments') #TODO
#    def _experiments_default(self):
#        from mcss_experiment import McssExperiment
#        return McssExperiment()
#    
#    # file:///home/jvb/src/ETS_3.4.0/AppTools/docs/html/preferences/PreferencesInEnvisage.html
#    
#    preferences = List(contributes_to='envisage.preferences')
#    def _preferences_default(self):
#        return ['file://%s' % os.path.join(ETSConfig.application_data, 'preferences.ini')]


    # Contributions to PythonShellPlugin 

    bindings = List(contributes_to=PythonShellPlugin.BINDINGS)
    def _bindings_default(self):
        return [
            {
                'version':infobiotics.__version__,
                'mcss':mcss,
                'mcss_results':mcss_results,
                'prism':prism,
                'mc2':mc2,
                'poptimizer':poptimizer,
                
            },
        ]

    # doesn't work because 'execute_source' method not found
#    commands = List(contributes_to=PythonShellPlugin.COMMANDS)
#    def _commands_default(self):
#        return [
#            'from infobiotics.api import *',
#            'import infobiotics',
#            'print infobiotics.__version__',
#            'print version'
#        ]
