from pyface.action.api import Action

class ExitAction(Action):
    ''' An action that exits the workbench. '''
    description = 'Exit the application' # A longer description of the action.
#    image = ImageResource('exit') # The action's image (displayed on tool bar tools etc).
    name = 'Exit' # The action's name (displayed on menus/tool bar tools etc).
    tooltip = 'Exit the application' # A short description of the action used for tooltip text etc.

    def perform(self, event):
        ''' Perform the action. '''
        self.window.application.exit()