from enthought.pyface.action.api import Action
#from enthought.traits.ui.menu import UndoAction, RedoAction, RevertAction
#from mcss_experiment_editor import McssExperimentEditor
#from infobiotics.dashboard.plugins.experiments.params_experiment_editor import ParamsExperimentEditor
from infobiotics.dashboard.mcss.api import McssDashboardExperiment

class McssExperimentAction(Action):
#    name = 'mcss'
    name = 'Simulation'
    tooltip = 'Multi-compartmental stochastic simulation of a model.'
    
    def perform(self, event=None):
        obj = McssDashboardExperiment(application=self.window.workbench.application)
#        self.window.workbench.edit(
#            obj=obj,
#            kind=ParamsExperimentEditor, #TODO
#            use_existing=False
#        )
        obj.edit()

## in simulator_results/actions.py
#from simulator_results import SimulationResultsDialog #TODO
#from editor import SimulatorResultsEditor
#
#class SimulatorResultsAction(Action):
#    name = 'mcss'
#    tooltip = 'Visualise mcss simulations.' #TODO
#    
#    def perform(self, event=None):
#        obj = SimulationResultsDialog()
#        if not obj.loaded: return # user cancelled load
#        self.window.workbench.edit(
#            obj=obj,
#            kind=SimulatorResultsEditor,
#            use_existing=False
#        )

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


#class UndoAction(Action):
#    id = 'infobiotics.dashboard.plugins.mcss.actions.UndoAction'
#    name = '&Undo'
#    tooltip = 'Undo the last change'
#    accelerator = 'Ctrl-z'
#
#    def perform(self, event=None):
#        active_editor = self.window.active_editor
#        if active_editor is not None:
#            if hasattr(active_editor, 'ui'):
#                ui = active_editor.ui
#                if ui.history is not None and ui.history.can_undo:
#                    ui.handler._on_undo(ui.info)
#            
#            
#class RedoAction(Action):
#    id = 'infobiotics.dashboard.plugins.mcss.actions.RedoAction'
#    name = '&Redo'
#    tooltip = 'Redo the previous undo action'
#    accelerator = 'Ctrl-y'
#
#    def perform(self, event=None):
#        active_editor = self.window.active_editor
#        if active_editor is not None:
#            if hasattr(active_editor, 'ui'):
#                ui = self.window.active_editor.ui
#                if ui.history is not None and ui.history.can_redo:
#                    ui.handler._on_redo(ui.info)
