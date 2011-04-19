# if run directly
if __name__ == '__main__':
    
    # set process title
    import setproctitle
    setproctitle.setproctitle('Infobiotics Dashboard')
    
    import infobiotics
    # done in import infobiotics
#    # set TraitsUI backend
#    from enthought.etsconfig.api import ETSConfig
#    ETSConfig.toolkit = 'qt4'

# fixes 'no handlers could be found for logger "enthought.envisage.plugin"'
import logging
class NullHandler(logging.Handler): # http://docs.python.org/library/logging.html#library-config
    def emit(self, record):
        pass
null_handler = NullHandler()
loggers = [
#    '',
    'enthought.pyface.workbench.workbench_window',
    'enthought.envisage.plugin',
]
for logger in loggers:
#    logging.getLogger(logger).addHandler(null_handler)#NullHandler())
    logging.getLogger(logger).addHandler(logging.StreamHandler())

# import plugins
from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
#from enthought.envisage.developer.developer_plugin import DeveloperPlugin
#from enthought.envisage.developer.ui.developer_ui_plugin import DeveloperUIPlugin
from enthought.plugins.python_shell.python_shell_plugin import PythonShellPlugin
#from enthought.plugins.ipython_shell.ipython_shell_plugin import IPythonShellPlugin # IPythonShellPlugin is not supported by Qt backend, yet.

#from infobiotics.dashboard.plugins.text_editor.text_editor_plugin import TextEditorPlugin
from enthought.plugins.text_editor.text_editor_plugin import TextEditorPlugin

#from enthought.envisage.ui.single_project.project_plugin import ProjectPlugin #TODO
from infobiotics.dashboard.core.ui_plugin import CoreUIPlugin
#from infobiotics.dashboard.plugins.example.ui_plugin import ExampleUIPlugin
#from infobiotics.dashboard.plugins.unified_open_action.unified_open_action_ui_plugin import UnifiedOpenActionUIPlugin
#from infobiotics.dashboard.plugins.bnf.ui_plugin import BNFUIPlugin
from infobiotics.dashboard.mcss.ui_plugin import McssUIPlugin
from infobiotics.dashboard.mcss.results.ui_plugin import McssResultsUIPlugin
from infobiotics.dashboard.pmodelchecker.ui_plugin import PModelCheckerUIPlugin
from infobiotics.dashboard.poptimizer.ui_plugin import POptimizerUIPlugin

from infobiotics.dashboard.app import InfobioticsDashboardWorkbenchApplication

def workbench_plugin_factory():
    '''Creates a WorkbenchPlugin that doesn't prompt on exit by default.'''
    from infobiotics.preferences import preferences
    preferences.set('default/enthought.envisage.ui.workbench.prompt_on_exit', False) # previously done in infobiotics.preferences
    # use our preferences instead of the pkgfile://enthought.envisage.ui.workbench/preferences.ini
    return WorkbenchPlugin(my_preferences=['file://%s' % preferences.filename]) # need 'file://' because this later gets split on '://' 

plugin_factories = [
    CorePlugin,
    workbench_plugin_factory,
#    DeveloperPlugin,
#    DeveloperUIPlugin,
    PythonShellPlugin,
#    IPythonShellPlugin,
    TextEditorPlugin,
#    ProjectPlugin, #TODO
    CoreUIPlugin,
#    UnifiedOpenActionUIPlugin,
#    BNFUIPlugin,
    McssUIPlugin,
    McssResultsUIPlugin,
    PModelCheckerUIPlugin,
    POptimizerUIPlugin,
]

def main(plugin_factories=plugin_factories):
    '''Main entry point for Infobiotics Dashboard.

    Creates the Workbench Application from a collection of plugins.
    '''

    # create application from plugins
    application = InfobioticsDashboardWorkbenchApplication(
        # create plugins by calling each plugin factory
        plugins=[plugin_factory() for plugin_factory in plugin_factories],
    )

#    window = application.active_window
#    print window
#    window.active_perspective = window.get_perspective_by_id('infobiotics.dashboard.plugins.experiments.ui_plugin.ExperimentsPerspective') 
    
    application.run()
    # This starts the application, starts the GUI event loop, and when that 
    # terminates, stops the application.

if __name__ == '__main__':
    main()
