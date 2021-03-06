from pyface.action.api import Action
from traits.api import Any, Property, Bool
from apptools.io.api import File
from editor.text_editor import TextEditor
from pyface.api import FileDialog, OK

class NewFileAction(Action):
    ''' Open a new file in the text editor. '''
    tooltip = "Create a new file for editing"
    description = "Create a new file for editing"

#    window = Any() # The WorkbenchWindow the action is attached to.

    def perform(self, event=None):
        self.window.workbench.edit(File(''), kind=TextEditor,
            use_existing=False)


class OpenFileAction(Action):
    ''' Open an existing file in the text editor. '''
#    tooltip = "Open a file for editing"
    description = "Open a file for editing"

    def perform(self, event=None):
        dialog = FileDialog(parent=self.window.control,
            title='Open File')
        if dialog.open() == OK:
            self.window.workbench.edit(File(dialog.path), kind=TextEditor)
    

class SaveFileAction(Action):
    ''' Save, overwriting, the current file in the text editor. '''
#    tooltip = "Save the current file"
    description = "Save the current file"
    window = Any()
    enabled = Property(Bool, depends_on='window.active_editor')
    def _get_enabled(self):
        if self.window.active_editor is not None:
            if hasattr(self.window.active_editor, 'save'):
                return True
        return False

    def perform(self, event=None):
        self.window.active_editor.save()


class SaveAsFileAction(Action):
    ''' Save the current file in the text editor. '''
#    tooltip = "Save the current file as another file"
    description = "Save the current file as another file"
    window = Any()
    enabled = Property(Bool, depends_on='window.active_editor')
    def _get_enabled(self):
        if self.window.active_editor is not None:
            if hasattr(self.window.active_editor, 'save_as'):
                return True
        return False

    def perform(self, event=None):
        self.window.active_editor.save_as()
