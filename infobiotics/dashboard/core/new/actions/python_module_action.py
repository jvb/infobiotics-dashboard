from pyface.action.api import Action
from apptools.io.api import File
from editors.api import PythonModuleEditor

class PythonModuleAction(Action):
    name = '&Python Module'
    description = 'Create a new Python module'
    accelerator = 'Ctrl-m'

    def perform(self, event=None):
        perform(self.window) # can't use 'on_perform = perform' because we can't pass window 

def perform(window):
    window.workbench.edit(
        File(''), 
        kind=PythonModuleEditor,
        use_existing=False,
    )
