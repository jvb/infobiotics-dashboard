#TODO obsolete with UnifiedOpenAction

from pyface.action.api import Action
from pyface.api import FileDialog, OK
from apptools.io.api import File
from editors.api import TextFileEditor

class OpenTextFileAction(Action):
    name = 'Open &Text File...'
    description = 'Open a text file'

    def perform(self, event=None):
        perform(self.window)

def perform(window):
    dialog = FileDialog(parent=window.control,
        title='Open Text File')
    if dialog.open() == OK:
        window.workbench.edit(
            File(dialog.path), 
            kind=TextFileEditor,
            use_existing=False, # this stops you opening the same file twice (TODO in the same window?)
        )