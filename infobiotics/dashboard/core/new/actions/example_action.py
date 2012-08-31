from enthought.pyface.action.api import Action
from enthought.traits.api import Property, Bool 
#from enthought.pyface.api import ImageResource

class ExampleAction(Action):
    '''
    if self.tooltip == '': self.tooltip = self.description
    '''
    name = 'Example' # The action's name (displayed on menus/tool bar tools etc).
    description = 'An example of an action.' # A longer description of the action.
    tooltip = 'Example action' # A short description of the action used for tooltip text etc. 
    accelerator = 'Ctrl-e' # case sensitive
#    image = ImageResource('example_without_extension') # The action's image (displayed on tool bar tools etc).

    enabled = Property(Bool) # overrides Action.enabled = Bool(True) # if depends_on='window.trait': window = Any() required
    def _get_enabled(self):
        ''' Override this method to conditionally disable the action. '''
        return True
    
    def perform(self, event=None):
        perform(self.window) 
        
def perform(window):
    ''' Demonstrates pattern that allows non-actions to mimic perform.'''
    raise NotImplementedError
