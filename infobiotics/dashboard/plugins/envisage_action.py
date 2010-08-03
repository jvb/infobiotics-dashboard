from enthought.pyface.action.api import Action
from enthought.envisage.ui.workbench.api import WorkbenchWindow
from enthought.traits.api import Instance#, Any

class EnvisageAction(Action):
    window = Instance(WorkbenchWindow)#Any()
    
    name = ''
    description = ''
#    tooltip = '' # if self.tooltip == '': self.tooltip = self.description
    accelerator = 'Ctrl-e' # case sensitive
    
    def perform(self, event=None):
        raise NotImplementedError
