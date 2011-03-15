__version__ = '0.0.1'

# use TraitsBackendQt instead of wx
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

# fixes 'no handlers could be found for logger "enthought.envisage.plugin"'
import logging
class NullHandler(logging.Handler): # http://docs.python.org/library/logging.html#library-config
    def emit(self, record):
        pass
logging.getLogger('enthought.envisage.plugin').addHandler(NullHandler())
logging.getLogger('enthought.pyface.workbench.workbench_window').addHandler(NullHandler())
logging.getLogger('enthought.pyface.workbench.i_view').addHandler(NullHandler())
logging.getLogger('enthought.pyface.ui.qt4.workbench.workbench_window_layout').addHandler(logging.StreamHandler())#NullHandler())

from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import ImageResource, AboutDialog, SplashScreen
from enthought.traits.api import on_trait_change

class Application(WorkbenchApplication):
    # implements IApplication and WorkbenchApplication interfaces

    id = 'id' # The application's globally unique Id.
    name = 'name %s' % __version__ # The name of the application (also used on window title bars etc)
#    icon = ImageResource('images/icon') # The icon used on window title bars etc #TODO

#    def _preferences_default(self): #TODO better way of doing this?
#        ''' Touch preferences file to make sure it exists. '''
#        from infobiotics.preferences import preferences
#        filename = preferences.filename
#        import os.path
#        if not os.path.exists(filename): 
#            open(filename, 'w').close() 
#        return preferences
    
    def _about_dialog_default(self):
        return None
#        return AboutDialog(
#            parent = self.workbench.active_window.control,
##            image = ImageResource('images/logo.png'), #TODO
#            additions = [
#                self.name,
#                'by',
#                'someone',
#                'with',
#                'someone else,',
#                'and',
#                'someone in charge'
#            ]
#        )    
    
    def _splash_screen_default(self): #TODO
        return None
#        return SplashScreen(
#            image             = ImageResource('images/logo'),
##            show_log_messages = True,
#        )

    @on_trait_change('workbench.active_window')
    def _workbench_active_window_changed(self):
        window = self.workbench.active_window
        if window is not None: 
#            for i in range(10):
#                from actions.untitled_text_file_action import perform as new_untitled_text_file
#                new_untitled_text_file(window)
#                from actions.python_module_action import perform as new_python_module
#                new_python_module(window)
            from actions.untitled_text_file_action import perform as new_untitled_text_file
            new_untitled_text_file(window)


def main():
    ''' Creates the Workbench Application from a collection of plugins. '''

    # import plugins
    from enthought.envisage.core_plugin import CorePlugin
    from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
    #from enthought.envisage.developer.developer_plugin import DeveloperPlugin
    #from enthought.envisage.developer.ui.developer_ui_plugin import DeveloperUIPlugin
    from enthought.plugins.python_shell.python_shell_plugin import PythonShellPlugin
    #from enthought.plugins.ipython_shell.ipython_shell_plugin import IPythonShellPlugin # IPythonShellPlugin is not supported by Qt backend, yet.
    ##from enthought.plugins.text_editor.text_editor_plugin import TextEditorPlugin
    #from infobiotics.dashboard.plugins.text_editor.text_editor_plugin import TextEditorPlugin
    from plugin import DashboardPlugin
    #from infobiotics.dashboard.plugins.core.ui_plugin import CoreUIPlugin
    #from infobiotics.dashboard.plugins.unified_open_action.unified_open_action_ui_plugin import UnifiedOpenActionUIPlugin
    #from infobiotics.dashboard.plugins.bnf.ui_plugin import BNFUIPlugin
    
    from default_action_set import DefaultActionSet
    
    application = Application(
        plugins=[
            CorePlugin(),
            
            # remove ExitAction icon and 
            # disable About action if about_dialog is None 
            # with amended default_action_set
            WorkbenchPlugin(my_action_sets=[DefaultActionSet]),

#            DeveloperPlugin(),
#            DeveloperUIPlugin(),
            PythonShellPlugin(),
#            IPythonShellPlugin(),
#            TextEditorPlugin(),

            DashboardPlugin(),

#            CoreUIPlugin(),

#            UnifiedOpenActionUIPlugin(),

#            BNFUIPlugin(),
        ]
    )

    # don't prompt on exit by default
#    application.workbench._preferences.prompt_on_exit = False
    application.workbench._preferences.preferences.set('default/prompt_on_exit', False) #TODO test
    
#    window.active_perspective = window.get_perspective_by_id('infobiotics.dashboard.plugins.experiments.ui_plugin.ExperimentsPerspective') 
        
    application.run()
    # This starts the application, starts the GUI event loop, and when that 
    # terminates, stops the application.
    

if __name__ == '__main__':
    main()
    