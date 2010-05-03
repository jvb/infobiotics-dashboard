# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: actions.py 366 2010-01-13 20:16:01Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/experiments/actions.py $
# $Author: jvb $
# $Revision: 366 $
# $Date: 2010-01-13 20:16:01 +0000 (Wed, 13 Jan 2010) $


from enthought.pyface.action.api import Action as PyFaceAction
from enthought.pyface.constant import * # OK, NO, CANCEL, YES


class NewExperimentAction(PyFaceAction):
    experiment_class = Class(ParamsExperiment) 
    def perform(self, event=None):
        obj = self.experiment_class(application=self.window.workbench.application)
        obj.edit_traits(kind='modal')

#class LoadExperimentAction(PyFaceAction):
#    experiment_class = Class(ParamsExperiment) 
class LoadExperimentAction(NewExperimentAction):
    def perform(self, event=None):
        obj = self.experiment_class(application=self.window.workbench.application)
        obj.load()
        obj.edit_traits(kind='modal')



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

            