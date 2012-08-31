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

# import plugins
from enthought.envisage.core_plugin import CorePlugin
from enthought.envisage.ui.workbench.workbench_plugin import WorkbenchPlugin
#from enthought.envisage.developer.developer_plugin import DeveloperPlugin
#from enthought.envisage.developer.ui.developer_ui_plugin import DeveloperUIPlugin
from enthought.plugins.python_shell.python_shell_plugin import PythonShellPlugin
#from enthought.plugins.ipython_shell.ipython_shell_plugin import IPythonShellPlugin # IPythonShellPlugin is not supported by Qt backend, yet.
##from enthought.plugins.text_editor.text_editor_plugin import TextEditorPlugin
#from infobiotics.dashboard.plugins.text_editor.text_editor_plugin import TextEditorPlugin
from plugin import FileEditorsPlugin
#from infobiotics.dashboard.plugins.core.ui_plugin import CoreUIPlugin
#from infobiotics.dashboard.plugins.unified_open_action.unified_open_action_ui_plugin import UnifiedOpenActionUIPlugin
#from infobiotics.dashboard.plugins.bnf.ui_plugin import BNFUIPlugin

# remove ExitAction icon and disable About action is about_dialog is None
from enthought.pyface.api import ImageResource
from enthought.pyface.action.api import Action

class ExitAction(Action):
    ''' An action that exits the workbench. '''
    description = 'Exit the application' # A longer description of the action.
#    image = ImageResource('exit') # The action's image (displayed on tool bar tools etc).
    name = 'Exit' # The action's name (displayed on menus/tool bar tools etc).
    tooltip = 'Exit the application' # A short description of the action used for tooltip text etc.

    def perform(self, event):
        ''' Perform the action. '''
        self.window.application.exit()

from enthought.pyface.action.api import Action
from enthought.traits.api import Any, Property, Bool

class AboutAction(Action):
    ''' An action that shows the 'About' dialog. '''
    description = 'Display information about the application'
    name = 'About'
    tooltip = 'Display information about the application'

    window = Any()
    
    enabled = Property(Bool, depends_on='window.application')
    def _get_enabled(self):
        if self.window is not None:
            if self.window.application.about_dialog is not None:
                return True
        return False

    def perform(self, event):
        ''' Perform the action. '''
        self.window.application.about()

from enthought.envisage.ui.action.api import Action, ActionSet, Menu
PKG = 'enthought.envisage.ui.workbench'#'.'.join(__name__.split('.')[:-1])
class DefaultActionSet(ActionSet):
    ''' The default workbench action set. '''
    menus = [
        Menu(
            name='&File', path='MenuBar',
            groups=['OpenGroup', 'SaveGroup', 'ImportGroup', 'ExitGroup']
        ),
        Menu(
            path='MenuBar',
            class_name='enthought.pyface.workbench.action.api:ViewMenuManager'
        ),
        Menu(
            name='&Tools', path='MenuBar',
            groups=['PreferencesGroup']
        ),
        Menu(
            name='&Help', path='MenuBar',
            groups=['AboutGroup']
        )
    ]
    actions = [
        Action(
            path='MenuBar/File', group='ExitGroup',
            class_name=__name__+':ExitAction'
        ),
        Action(
            path='MenuBar/Tools', group='PreferencesGroup',
            class_name=PKG + '.action.api:EditPreferencesAction'
        ),
        Action(
            path='MenuBar/Help', group='AboutGroup',
            class_name=__name__+':AboutAction'
        ),
    ]


from enthought.envisage.ui.workbench.api import WorkbenchApplication
from enthought.pyface.api import ImageResource, AboutDialog, SplashScreen

__version__ = '0.0.1'

class TestWorkbenchApplication(WorkbenchApplication):
    # implements IApplication and WorkbenchApplication interfaces

    id = 'id' # The application's globally unique Id.
    name = 'name %s' % __version__ # The name of the application (also used on window title bars etc)
#    icon = ImageResource('images/icon.png') # The icon used on window title bars etc #TODO
    
#    def _preferences_default(self):
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


def main():
    ''' Creates the Workbench Application from a collection of plugins. '''

    application = TestWorkbenchApplication(
        plugins=[
            CorePlugin(),
            WorkbenchPlugin(my_action_sets=[DefaultActionSet]),

#            DeveloperPlugin(),
#            DeveloperUIPlugin(),
            PythonShellPlugin(),
#            IPythonShellPlugin(),
#            TextEditorPlugin(),

            FileEditorsPlugin(),

#            CoreUIPlugin(),

#            UnifiedOpenActionUIPlugin(),

#            BNFUIPlugin(),
        ]
    )

    # don't prompt on exit by default
    application.workbench._preferences.prompt_on_exit = False
    
#    window = application.active_window
#    window.active_perspective = window.get_perspective_by_id('infobiotics.dashboard.plugins.experiments.ui_plugin.ExperimentsPerspective') 
    
    application.run()
    # This starts the application, starts the GUI event loop, and when that 
    # terminates, stops the application.
    

if __name__ == '__main__':
    main()
    