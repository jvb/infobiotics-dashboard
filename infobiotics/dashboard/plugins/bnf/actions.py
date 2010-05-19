from enthought.pyface.action.api import Action as PyFaceAction
from enthought.pyface.constant import * # OK, NO, CANCEL, YES
from enthought.io.api import File
from enthought.pyface.api import FileDialog, OK
from infobiotics.dashboard.plugins.bnf.bnf_editor import BNFEditor
from infobiotics.dashboard.plugins.bnf.lpp_editor import LPPEditor
from infobiotics.dashboard.plugins.bnf.sps_editor import SPSEditor
from infobiotics.dashboard.plugins.bnf.lat_editor import LATEditor
from infobiotics.dashboard.plugins.bnf.plb_editor import PLBEditor 

from enthought.traits.api import Class, Str

class NewFileAction(PyFaceAction):
    ''' Superclass for new file actions.

    Override editor to specify the editor class to use.
    
    '''
    id = 'infobiotics.dashboard.plugins.bnf.actions.NewFileAction'
    name = 'New'
    tooltip = 'Create a new file'
    editor = Class
    
    def perform(self, event=None):
        self.window.workbench.edit(
            obj=File(''), 
            kind=self.editor,
            use_existing=False
        )


class OpenFileAction(NewFileAction):
    ''' Superclass for open file actions.

    Override editor to specify the editor class to use.
    
    Override wildcard to specify the wildcard string to when looking for files,
    e.g. 'Text file (*.txt)'
    
    Override title to specify an alternative title for the 'Open File' dialog.
    
    '''
    name = 'Open'
    tooltip = 'Open a file'
    wildcard = Str
    title = Str('Open File')
    
    def perform(self, event=None, path=None):
#        logger.info('OpenFileAction.perform()')
        if path is None:
            dialog = FileDialog(
                parent=self.window.control,
                title=self.title,
                wildcard=self.wildcard
            )
            if dialog.open() == OK:
                self.window.workbench.edit(
                    File(dialog.path),
                    kind=self.editor
                )
        else:
            self.window.workbench.edit(
                File(path),
                kind=self.editor
            )
            
            
class NewLPPAction(NewFileAction):
    id = 'infobiotics.dashboard.plugins.bnf.NewLPPAction'
    name = 'New LPP'
    tooltip = 'Create a new Lattice Population P system BNF file'
    editor = LPPEditor

class OpenLPPAction(OpenFileAction):
    name = 'Open LPP'
    tooltip = "Open a Lattice Population P system BNF file for editing"
    editor = LPPEditor
    wildcard = 'Lattice Population P system (*.lpp)'


class NewSPSAction(NewFileAction):
    name = 'New SPS'
    tooltip = 'Create a new Stochastic P system BNF file'
    editor = SPSEditor

class OpenSPSAction(OpenFileAction):
    name = 'Open SPS'
    tooltip = "Open a Stochastic P system BNF file for editing"
    editor = SPSEditor
    wildcard = 'Stochastic P system (*.sps)'
    
    
class NewLATAction(NewFileAction):
    name = 'New LAT'
    tooltip = 'Create a new lattice BNF file'
    editor = LATEditor

class OpenLATAction(OpenFileAction):
    name = 'Open LAT'
    tooltip = "Open a lattice BNF file for editing"
    editor = LATEditor
    wildcard = 'Lattice (*.lat)'


class NewPLBAction(NewFileAction):
    name = 'New PLB'
    tooltip = 'Create a new P system module library BNF file'
    editor = PLBEditor

class OpenPLBAction(OpenFileAction):
    name = 'Open PLB'
    tooltip = "Open a P system module library BNF file for editing"
    editor = PLBEditor
    wildcard = 'P system module library (*.plb)'


    



#class NewViewAction(PyFaceAction):
#    """ An action that dynamically creates and adds a view. """
#
#    # 'Action' interface
#    description = 'Create and add a new view' # A longer description of the action
#    name = 'New View' # The action's name (displayed on menus/tool bar tools etc)
#    tooltip = 'Create and add a new view' # A short description of the action used for tooltip text etc
#
#    def perform(self, event):
#        # You can give the view a position... (it default to 'left')...
#        view = PyFaceWorkbenchView(id='my.view.fred', name='Fred', position='right')
#        self.window.add_view(view) # is window part of the handler context?
#
#        # or you can specify it on the call to 'add_view'...
#        view = PyFaceWorkbenchView(id='my.view.wilma', name='Wilma')
#        self.window.add_view(view, position='top') # is window part of the handler context?

            
class SaveAction(PyFaceAction):
    ''' ...

    '''
    name = '&Save'
    tooltip = 'Save the current file'
    description = 'Save the current file'
    
    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            active_editor.save()

        

class SaveAsAction(PyFaceAction):
    ''' ...
    
    '''
    name = 'Save &As...'
    tooltip = 'Save as another file'
    description = 'Save as another file'

    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            active_editor.save_as()

from os.path import basename
def close_prompting_to_save_if_dirty(self, editor):
    if isinstance(editor, BNFEditor):
        if editor._dirty:
            if len(editor.obj.path) != 0:
                message = "'%s' has been modified. Save changes?" % basename(editor.obj.path)
            else:
                message = "Contents have been modified. Save?" 
            result = self.window.workbench.confirm(message,
                title='Save File', cancel=True, default=CANCEL
            )
            if result == YES:
                editor.save_as()
            elif result == CANCEL:
                return
            elif result == NO:
                pass
        editor.close()


class CloseAction(PyFaceAction):
    ''' ...
    
    '''
    name = '&Close'
    tooltip = "Close the current editor"
    description = "Close the current editor"
    
    def perform(self, event=None):
        active_editor = self.window.active_editor
        close_prompting_to_save_if_dirty(self, active_editor)


class CloseAllAction(PyFaceAction):
    ''' ...
    
    '''
    name = 'C&lose All'
    tooltip = "Close all open editors"
    description = tooltip
    
    def perform(self, event=None):
        while len(self.window.editors) > 0:
            editor = self.window.editors[0]
            close_prompting_to_save_if_dirty(self, editor)


#class PrintSelectionAction(PyFaceAction):
#    ''' ...
#
#    '''
#    name = '&Print Selection'
#    tooltip = ''
#    description = ''
#    
#    def perform(self, event=None):
#        active_editor = self.window.active_editor
#        if active_editor is not None:
#            print active_editor.selection
            