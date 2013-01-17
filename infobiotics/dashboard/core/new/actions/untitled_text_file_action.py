from pyface.action.api import Action
from apptools.io.api import File
from editors.api import TextFileEditor

class UntitledTextFileAction(Action):
    name = '&Untitled Text File'
    description = 'Create a new text file'
    accelerator = 'Ctrl-t'

    def perform(self, event=None):
        perform(self.window) # can't use 'on_perform = perform' because we can't pass window 

def perform(window):
    window.workbench.edit(
        File(''), 
        kind=TextFileEditor,
        use_existing=False,
    )

