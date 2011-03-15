from enthought.pyface.action.api import Action# as PyFaceAction
from enthought.envisage.ui.workbench.api import WorkbenchWindow
from enthought.traits.api import Any, Property, Bool 

#class Action(PyFaceAction):
#    ''' Extends PyFace Action with 'window' and 'enabled'. '''
#    name = ''
#    description = ''
##    tooltip = '' # if self.tooltip == '': self.tooltip = self.description
#    accelerator = 'Ctrl-e' # case sensitive
#    window = Any()
#    enabled = Property(Bool) # overrides Action.enabled = Bool(True)
#    def _get_enabled(self):
#        ''' Override this method to conditionally disable the action. '''
#        return True
#    
#    def perform(self, event=None):
#        perform_envisage_action(self.window) 
        
def perform_envisage_action(window):
    ''' Demonstrates pattern that allows non-actions to mimic perform.'''
    raise NotImplementedError

from enthought.io.api import File
from api import TextFileEditor, PythonModuleEditor, AbstractFileEditor
from enthought.pyface.api import FileDialog, OK
from enthought.traits.api import Any

#import logging
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.DEBUG)

def untitled_text_file(window):
    window.workbench.edit(
        File(''), 
        kind=TextFileEditor,
        use_existing=False,
    )

class UntitledTextFileAction(Action):
    ''' Create a new text file. '''
    name = '&Untitled Text File'
    tooltip = "Create a new text file" #TODO only used in toolbar?
    description = "Create a new text file"

    window = Any() # The WorkbenchWindow the action is attached to.

    def perform(self, event=None):
#        logger.info('UntitledTextFileAction.perform()')
        untitled_text_file(self.window) # can't use 'on_perform = untitled_text_file' because we can't pass window 

class PythonModuleAction(Action):
    ''' Create a new Python module. '''
    name = '&Python module'
    description = "Create a new Python module"

    def perform(self, event=None):
        self.window.workbench.edit(
            File(''), 
            kind=PythonModuleEditor,
            use_existing=False,
        )
        
#class OpenAction(Action): #TODO
#    name = '&Open...'

class OpenTextFileAction(Action): # TODO remove to UnifiedOpenDialog
    ''' Open an existing file in an text editor. '''
    name = 'Open &Text File...'
#    tooltip = "Open a file for editing"
    description = "Open a file for editing"

    #TODO why doesn't this action need a window trait like 'window = Any()' here? 

    def perform(self, event=None):
        dialog = FileDialog(parent=self.window.control,
            title='Open File')
        if dialog.open() == OK:
            self.window.workbench.edit(
                File(dialog.path), 
                kind=TextFileEditor,
#                use_existing=False, # maybe this stops it opening the same file twice?
            )

class SaveAction(Action):
    ''' Save, overwriting, the contents of the active editor. '''
    name = '&Save'
#    tooltip = "Save the current file"
    description = "Save the current file"
    
    window = Any()
    
    enabled = Property(Bool, depends_on='window.active_editor')
    def _get_enabled(self):
        if self.window.active_editor is not None:
            if isinstance(self.window.active_editor, AbstractFileEditor):
                return True
        return False

    def perform(self, event=None):
        self.window.active_editor.save()

class SaveAsAction(SaveAction):
    ''' Save the contents of the active editor. '''
    name = 'Save &As...'
#    tooltip = "Save the current file as another file"
    description = "Save the current file as another file"

    def perform(self, event=None):
        self.window.active_editor.save_as()

#TODO Close and Close All
