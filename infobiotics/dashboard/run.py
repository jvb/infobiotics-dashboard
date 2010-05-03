from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
ETSConfig.company = 'infobiotics'
from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
from enthought.envisage.developer.developer_plugin import DeveloperPlugin
from enthought.envisage.developer.ui.developer_ui_plugin import DeveloperUIPlugin
from enthought.plugins.text_editor.text_editor_plugin import TextEditorPlugin
from enthought.plugins.python_shell.python_shell_plugin import PythonShellPlugin
#from enthought.plugins.ipython_shell.ipython_shell_plugin import IPythonShellPlugin # IPythonShellPlugin is not supported by Qt backend, yet.
#from enthought.envisage.ui.single_project.project_plugin import ProjectPlugin
from infobiotics.dashboard.app import InfobioticsDashboardWorkbenchApplication
from infobiotics.dashboard.plugins.experiments.ui_plugin import ExperimentsUIPlugin
from infobiotics.dashboard.plugins.mcss.ui_plugin import McssUIPlugin
from infobiotics.dashboard.plugins.pmodelchecker.ui_plugin import PModelCheckerUIPlugin
#from infobiotics.dashboard.plugins.poptimizer.ui_plugin import POptimizerUIPlugin
#from infobiotics.dashboard.plugins.bnf.ui_plugin import BNFUIPlugin
from infobiotics.dashboard.plugins.simulator_results.ui_plugin import SimulatorResultsUIPlugin
#from infobiotics.dashboard.plugins.example.ui_plugin import ExampleUIPlugin
#from infobiotics.dashboard.plugins.unified_open_action.unified_open_action_ui_plugin import UnifiedOpenActionUIPlugin

def main():
    ''' Main entry point for Infobiotics Dashboard.

    Creates the Workbench Application from a collection of plugins.
    
    '''
    application = InfobioticsDashboardWorkbenchApplication(
        
        plugins=[
            CorePlugin(),
            WorkbenchPlugin(),

#            DeveloperPlugin(),
#            DeveloperUIPlugin(),
#            PythonShellPlugin(),
#            IPythonShellPlugin(),
            TextEditorPlugin(),

#            ProjectPlugin(),

            ExperimentsUIPlugin(),
            McssUIPlugin(),
            PModelCheckerUIPlugin(),
#            POptimizerUIPlugin(),
            
            SimulatorResultsUIPlugin(),
#            McssResultsUIPlugin(),
#            UnifiedOpenActionUIPlugin(),

#            BNFUIPlugin(),

##            McssPlugin(), # testing Envisage services, see mcss_plugin docstring
         
#            ExampleUIPlugin(),   
        ]
    )

#    application.setup() #TEST called automatically
    
#    from enthought.preferences.api import set_default_preferences, ScopedPreferences
#    set_default_preferences(ScopedPreferences(filename='preferences.ini'))
#    application.preferences.dump()

#    window = application.active_window
#    print window
#    window.active_perspective = window.get_perspective_by_id('infobiotics.dashboard.plugins.experiments.ui_plugin.ExperimentsPerspective') 
    
    application.run()
    # This starts the application, starts the GUI event loop, and when that 
    # terminates, stops the application.
    

if __name__ == '__main__':
    main()
