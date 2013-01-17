from pyface.action.api import Action
from traitsui.menu import UndoAction, RedoAction, RevertAction
from pyface.constant import * # OK, NO, CANCEL, YES

class UndoAction(Action):
    id = 'envisage.plugins.generic.actions.UndoAction'
    name = '&Undo'
    tooltip = 'Undo the last change'
    accelerator = 'Ctrl-z' # case sensitive
    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            if hasattr(active_editor, 'ui'): # TraitsUIEditors
                ui = active_editor.ui
                if ui.history is not None and ui.history.can_undo:
                    ui.handler._on_undo(ui.info)
#                elif #TODO establish Undo pattern for non-TraitUIEditors
                            
class RedoAction(Action):
    id = 'infobiotics.dashboard.mcss.actions.RedoAction'
    name = '&Redo'
    tooltip = 'Redo the previous undo action'
    accelerator = 'Ctrl-y'
    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            if hasattr(active_editor, 'ui'): # TraitsUIEditors
                ui = self.window.active_editor.ui
                if ui.history is not None and ui.history.can_redo:
                    ui.handler._on_redo(ui.info)
#                elif #TODO establish Redo pattern for non-TraitUIEditors, same as Undo pattern
            
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


class CloseAction(PyFaceAction):
    ''' ...
    
    '''
    name = '&Close'
    tooltip = "Close the current editor"
    description = "Close the current editor"
    
    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            if active_editor._dirty:
                file = '%s%s' % (active_editor.obj.name, active_editor.obj.ext)
                if file != '':
                    message = "'%s' has been modified. Save changes?" % file
                else:
                    message = "Contents have been modified. Save?" 
                result = self.window.workbench.confirm(message,
                    title='Save File', cancel=True, default=CANCEL
                )
                if result == YES:
                    active_editor.save_as()
                elif result == CANCEL:
                    return
                elif result == NO:
                    pass
            active_editor.close()


class CloseAllAction(PyFaceAction):
    ''' ...
    
    '''
    name = 'C&lose All'
    tooltip = "Close all open editors"
    description = tooltip
    
    def perform(self, event=None):
        while len(self.window.editors) > 0:
            editor = self.window.editors[0]
#            print editor
            if editor is not None:
                if editor._dirty:
                    file = '%s%s' % (editor.obj.name, editor.obj.ext)
                    if file != '':
                        message = "'%s' has been modified. Save changes?" % file
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