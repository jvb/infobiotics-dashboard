from enthought.pyface.action.api import Action
from enthought.traits.api import Any, Property, Bool
from enthought.io.api import File
from editor.text_editor import TextEditor
from enthought.pyface.api import FileDialog, OK

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class NewFileAction(Action):
    ''' Open a new file in the text editor. '''
    tooltip = "Create a new file for editing"
    description = "Create a new file for editing"

    window = Any() # The WorkbenchWindow the action is attached to.

    def perform(self, event=None):
        logger.info('NewFileAction.perform()')
        self.window.workbench.edit(File(''), kind=TextEditor,
            use_existing=False)


class OpenFileAction(Action):
    ''' Open an existing file in the text editor. '''
#    tooltip = "Open a file for editing"
    description = "Open a file for editing"

    #TODO why doesn't this action need a window trait? 

    def perform(self, event=None):
        logger.info('OpenFileAction.perform()')
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
        logger.info('SaveFileAction.perform()')
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
        logger.info('SaveAsFileAction.perform()')
        self.window.active_editor.save_as()
