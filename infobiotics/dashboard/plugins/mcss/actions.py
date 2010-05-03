# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: actions.py 411 2010-01-25 18:03:26Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/mcss/actions.py $
# $Author: jvb $
# $Revision: 411 $
# $Date: 2010-01-25 18:03:26 +0000 (Mon, 25 Jan 2010) $


from enthought.traits.ui.menu import UndoAction, RedoAction, RevertAction
from enthought.pyface.action.api import Action
#from mcss_experiment_editor import McssExperimentEditor
#from infobiotics.dashboard.plugins.experiments.params_experiment_editor import ParamsExperimentEditor
#from mcss_experiment import McssExperiment
from infobiotics.api import McssExperiment


class McssExperimentAction(Action):
    id = 'infobiotics.dashboard.plugins.mcss.actions:NewMcssExperimentAction'
    name = 'Stochastic simulation (mcss)'
    tooltip = 'Perform a simulation experiment with mcss'
    
    def perform(self, event=None):
        obj=McssExperiment(application=self.window.workbench.application)
#        self.window.workbench.edit(
#            obj=obj,
#            kind=ParamsExperimentEditor,
#            use_existing=False
#        )
        obj.edit()


#class LoadMcssParametersAction(PyFaceAction): #TODO
#    ''' ... 
#    '''
#    id = 'infobiotics.dashboard.plugins.mcss.actions.LoadMcssParametersAction'
#    name = 'Load mcss parameters'
#    tooltip = ''
#    
#    def perform(self, event=None):
#        raise NotImplementedError
#                
#    
#class SaveMcssParametersAction(PyFaceAction): #TODO
#    ''' ... 
#    '''
#    id = 'infobiotics.dashboard.plugins.mcss.actions.SaveMcssParametersAction'
#    name = 'Save mcss parameters'
#    tooltip = ''
#    
#    def perform(self, event=None):
#        raise NotImplementedError


class UndoAction(Action):
    id = 'infobiotics.dashboard.plugins.mcss.actions.UndoAction'
    name = '&Undo'
    tooltip = 'Undo the last change'
    accelerator = 'Ctrl-z'

    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            if hasattr(active_editor, 'ui'):
                ui = active_editor.ui
                if ui.history is not None and ui.history.can_undo:
                    ui.handler._on_undo(ui.info)
            
            
class RedoAction(Action):
    id = 'infobiotics.dashboard.plugins.mcss.actions.RedoAction'
    name = '&Redo'
    tooltip = 'Redo the previous undo action'
    accelerator = 'Ctrl-y'

    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            if hasattr(active_editor, 'ui'):
                ui = self.window.active_editor.ui
                if ui.history is not None and ui.history.can_redo:
                    ui.handler._on_redo(ui.info)
