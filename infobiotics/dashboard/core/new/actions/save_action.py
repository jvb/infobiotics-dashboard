from pyface.action.api import Action
from traits.api import Property, Bool, Any
from editors.api import AbstractFileEditor

class SaveAction(Action):
    name = '&Save'
    description = 'Save, overwriting, the contents of the active editor.'
    tooltip = 'Save (Ctrl-S)'
    accelerator = 'Ctrl-s'
    window = Any
    enabled = Property(Bool, depends_on='window:active_editor')
    def _get_enabled(self):
        if self.window.active_editor is not None and isinstance(self.window.active_editor, AbstractFileEditor):
            return True
        return False

    def perform(self, event=None):
        perform(self.window)
        
def perform(window):
    window.active_editor.save()
